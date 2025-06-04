import os
# -- Disable the ROS2 Bridge extension early before any Isaac Sim or Omniverse modules are imported --
os.environ["OMNI_DISABLE_EXTENSIONS"] = "omni.isaac.ros2_bridge"

#
# IMPORTANT: Instantiate SimulationApp before importing other Omniverse or PXR modules.
from isaacsim import SimulationApp

simulation_app = SimulationApp({
    "headless": False,
    "hide_ui": True,
    "active_gpu": 0,
    "physics_gpu": 0,
    "multi_gpu": False,
    "max_gpu_count": 2,
    "sync_loads": True,
    "width": 1280,
    "height": 720,
    "window_width": 1280,
    "window_height": 720,
    "display_options": 3094,
    "subdiv_refinement_level": 0,
    "renderer": "RayTracedLighting",
    "anti_aliasing": 4,
    "samples_per_pixel_per_frame": 32,
    "denoiser": True,
    "max_bounces": 2,
    "max_specular_transmission_bounces": 2,
    "max_volume_bounces": 2,
    "fast_shutdown": True,
    "extensionsToDisable": ["omni.isaac.ros2_bridge"]
})

# ----------------------------------------------------------------
# Now import all remaining modules
# ----------------------------------------------------------------
import carb
import omni.timeline
from omni.isaac.core.world import World
from omni.isaac.core.utils.viewports import set_camera_view

# Pegasus simulator and drone-related modules
from pegasus.simulator.params import ROBOTS, SIMULATION_ENVIRONMENTS
from pegasus.simulator.logic.vehicles.multirotor import Multirotor, MultirotorConfig
from pegasus.simulator.logic.interface.pegasus_interface import PegasusInterface

# Correct import for the MonocularCamera sensor
from pegasus.simulator.logic.graphical_sensors.monocular_camera import MonocularCamera

# Import the custom python control backend (ensuring proper path resolution)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + '/utils')
from nonlinear_controller import NonlinearController

# Auxiliary modules
from scipy.spatial.transform import Rotation
import numpy as np
import cv2
from pathlib import Path

# USD libraries for lighting modifications
from pxr import UsdLux
import omni.usd

class PegasusApp:
    """
    PegasusApp sets up the simulation, spawns a drone with an attached camera sensor,
    and records the camera output to a video file.
    """
    def __init__(self):
        # Acquire the timeline for simulation control
        self.timeline = omni.timeline.get_timeline_interface()

        # Start the Pegasus Interface and create the simulation world
        self.pg = PegasusInterface()
        self.pg._world = World(**self.pg._world_settings)
        self.world = self.pg.world

        # Load the Warehouse environment
        self.pg.load_environment(SIMULATION_ENVIRONMENTS["Curved Gridroom"])

        # Set a custom camera view for the viewport
        set_camera_view(eye=(15, 10, 10), target=(7.5, 0, 3))

        # --- Modify Lighting: Switch to Global (Dome) Lighting ---
        stage = omni.usd.get_context().get_stage()
        default_light = stage.GetPrimAtPath("/World/defaultLight")
        if default_light:
            default_light.GetAttribute("intensity").Set(0.0)
        dome_light_path = "/World/DomeLight"
        if not stage.GetPrimAtPath(dome_light_path):
            dome_light = UsdLux.DomeLight.Define(stage, dome_light_path)
            dome_light.CreateIntensityAttr().Set(5000.0)
            dome_light.CreateColorAttr().Set((1.0, 1.0, 1.0))
        # --- End Lighting Modification ---

        # Get the current directory for trajectory and result files
        self.curr_dir = str(Path(os.path.dirname(os.path.realpath(__file__))).resolve())

        # Create the drone vehicle with a custom nonlinear controller backend
        config_multirotor1 = MultirotorConfig()
        config_multirotor1.backends = [NonlinearController(
            trajectory_file=os.path.join(self.curr_dir, "trajectories", "pitch_relay_90_deg_2.csv"),
            results_file=os.path.join(self.curr_dir, "results", "single_statistics.npz"),
            Ki=[0.5, 0.5, 0.5],
            Kr=[2.0, 2.0, 2.0]
        )]

        self.drone = Multirotor(
            "/World/quadrotor1",
            ROBOTS['Iris'],
            0,
            [2.3, -1.5, 0.07],
            Rotation.from_euler("XYZ", [0.0, 0.0, 0.0], degrees=True).as_quat(),
            config=config_multirotor1,
        )

        # Reset the simulation to properly initialize all vehicles
        self.world.reset()

        # ----------------------------
        # Set up and attach the camera
        # ----------------------------
        camera_config = {
            "depth": True,
            "position": np.array([0.30, 0.0, 0.0]),  # offset relative to the drone body
            "orientation": np.array([0.0, 0.0, 0.0]),  # Euler angles in degrees (ZYX order)
            "resolution": (1280, 720),  # width, height
            "frequency": 30,          # capture frequency in Hz
            "intrinsics": np.array([[958.8, 0.0, 957.8],
                                    [0.0, 956.7, 589.5],
                                    [0.0, 0.0, 1.0]]),
            "distortion_coefficients": np.array([0.14, -0.03, -0.0002, -0.00003, 0.009, 0.5, -0.07, 0.017]),
            "diagonal_fov": 140.0
            # Optionally, you might try adding a parameter such as "use_device_buffer": True if supported.
        }
        # Create and attach the MonocularCamera sensor to the drone
        self.camera = MonocularCamera("camera", camera_config)
        self.camera.initialize(self.drone)
        self.camera.start()

        # Initialize OpenCV VideoWriter for recording video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_path = os.path.join(self.curr_dir, "results", "drone_camera_output.avi")
        self.video_writer = cv2.VideoWriter(
            self.video_path,
            fourcc,
            30,  # frame rate
            camera_config["resolution"]
        )

    def run(self):
        """
        Main simulation loop. Uses the best-available method to retrieve camera frames.
        If the optimized device-buffer copy API is available, it will be used;
        otherwise, it falls back to get_rgba() (which may trigger the synthetic data warning).
        """
        self.timeline.play()

        # Extract resolution from the camera configuration (width, height)
        width, height = self.camera._resolution

        while simulation_app.is_running():
            # Step the simulation with rendering enabled
            self.world.step(render=True)

            if hasattr(self.camera, "_camera") and self.camera._camera is not None:
                # Check for optimized methods (which may not be available in your version)
                if (hasattr(self.camera._camera, "copy_texture_to_device_buffer") and
                    hasattr(self.camera._camera, "get_rgba_from_device_buffer")):
                    self.camera._camera.copy_texture_to_device_buffer()  # Optimized device-buffer copy
                    raw_frame = self.camera._camera.get_rgba_from_device_buffer()
                else:
                    raw_frame = self.camera._camera.get_rgba()

                if raw_frame is not None and raw_frame.size == (width * height * 4):
                    # Reshape and extract the RGB channels (discard alpha)
                    frame = raw_frame.reshape((height, width, 4))[:, :, :3]
                    if frame.dtype != np.uint8:
                        frame = (255 * frame).astype(np.uint8)
                    self.video_writer.write(frame)

        # Cleanup: release video file, log warning, stop timeline, and close simulation.
        self.video_writer.release()
        carb.log_warn("PegasusApp Simulation App is closing.")
        self.timeline.stop()
        simulation_app.close()

def main():
    app = PegasusApp()
    app.run()

if __name__ == "__main__":
    main()
