#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# ------------------------------------------------------------------------
# 1) CONFIGURE YOUR PATHS HERE
# ------------------------------------------------------------------------
BASE_DIR       = Path(__file__).resolve().parent
USD_PATH       = BASE_DIR / "outputs" / "fine_omni" / "export_scene.blend" / "export_scene.usdc"
# USD_PATH       = BASE_DIR / "outputs" / "fine_omni" / "smtn2.usdc"
TRAJECTORY_CSV = BASE_DIR / "trajectories" / "pitch_relay_90_deg_2.csv"
RESULTS_FILE   = BASE_DIR / "results" / "single_statistics.npz"
VIDEO_OUTPUT   = BASE_DIR / "results" / "drone_camera_output.avi"

# Early sanity checks – exit if anything is missing
for path, name in [
    (USD_PATH, "USD_PATH"),
    (TRAJECTORY_CSV, "TRAJECTORY_CSV"),
    (RESULTS_FILE, "RESULTS_FILE"),
]:
    if not path.exists():
        print(f"❌ ERROR: {name} not found at {path}")
        sys.exit(1)

# -- Disable the ROS2 Bridge extension early before Omniverse or PXR modules load --
os.environ["OMNI_DISABLE_EXTENSIONS"] = "omni.isaac.ros2_bridge"

#
# IMPORTANT: Instantiate SimulationApp before importing any other Omniverse or PXR modules.
#
from isaacsim import SimulationApp

simulation_app = SimulationApp({

    "headless": False,           # set True for headless runs
    "hide_ui": False,            # set True to hide UI even when headless=False
    "active_gpu": 0,             # GPU for rendering
    "physics_gpu": 0,            # GPU for physics
    "multi_gpu": False,
    "max_gpu_count": 2,
    "sync_loads": True,          # pause rendering until USD finishes loading
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

import carb
import omni.timeline
from omni.isaac.core.world import World
from omni.isaac.core.utils.stage import open_stage
from omni.isaac.core.utils.viewports import set_camera_view

from pegasus.simulator.params import ROBOTS
from pegasus.simulator.logic.vehicles.multirotor import Multirotor, MultirotorConfig
from pegasus.simulator.logic.interface.pegasus_interface import PegasusInterface
from pegasus.simulator.logic.graphical_sensors.monocular_camera import MonocularCamera

sys.path.insert(0, str(BASE_DIR / "utils"))
from nonlinear_controller import NonlinearController

from scipy.spatial.transform import Rotation
import numpy as np
import cv2
from pxr import UsdLux
import omni.usd

class PegasusApp:

    def __init__(self):

        if not open_stage(usd_path=str(USD_PATH)):

            print(f"Failed to load USD environment: {USD_PATH}")
            simulation_app.close()
            sys.exit(1)
            
        print(f"Loaded USD environment: {USD_PATH}")

        # --- Switch to Global (Dome) Lighting ---
        stage = omni.usd.get_context().get_stage()
        if prim := stage.GetPrimAtPath("/World/defaultLight"):
            prim.GetAttribute("intensity").Set(0.0)
        dome_path = "/World/DomeLight"
        if not stage.GetPrimAtPath(dome_path):
            dome = UsdLux.DomeLight.Define(stage, dome_path)
            dome.CreateIntensityAttr().Set(5000.0)
            dome.CreateColorAttr().Set((1.0, 1.0, 1.0))
        # --- End Lighting Modification ---

        # Initialize timeline and Pegasus world
        self.timeline = omni.timeline.get_timeline_interface()
        self.pg       = PegasusInterface()
        self.pg._world = World(**self.pg._world_settings)
        self.world     = self.pg.world

        # Position the viewport camera
        set_camera_view(eye=(15, 10, 10), target=(7.5, 0, 3))

        # Configure and spawn the drone with your nonlinear controller
        config = MultirotorConfig()
        config.backends = [
            NonlinearController(
                trajectory_file=str(TRAJECTORY_CSV),
                results_file=str(RESULTS_FILE),
                Ki=[0.5, 0.5, 0.5],
                Kr=[2.0, 2.0, 2.0]
            )
        ]
        self.drone = Multirotor(
            "/World/quadrotor1",
            ROBOTS['Iris'],
            0,
            [2.3, -1.5, 0.07],
            Rotation.from_euler("XYZ", [0.0, 0.0, 0.0], degrees=True).as_quat(),
            config=config
        )

        self.world.reset()

        # Set up camera sensor and video writer
        cam_cfg = {
            "depth": True,
            "position":  np.array([0.30, 0.0, 0.0]),
            "orientation": np.array([0.0, 0.0, 0.0]),
            "resolution": (1280, 720),
            "frequency": 30,
            "intrinsics": np.array([[958.8, 0.0, 957.8],
                                    [0.0, 956.7, 589.5],
                                    [0.0, 0.0, 1.0]]),
            "distortion_coefficients": np.array([0.14, -0.03, -0.0002, -0.00003, 0.009, 0.5, -0.07, 0.017]),
            "diagonal_fov": 140.0
        }
        self.camera = MonocularCamera("camera", cam_cfg)
        self.camera.initialize(self.drone)
        self.camera.start()

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(
            str(VIDEO_OUTPUT), fourcc, 30, cam_cfg["resolution"]
        )

    def run(self):
        self.timeline.play()
        w, h = self.camera._resolution
        try:
            while simulation_app.is_running():

                self.world.step(render=True)

                cam = self.camera._camera
                if hasattr(cam, "copy_texture_to_device_buffer"):
                    cam.copy_texture_to_device_buffer()
                    raw = cam.get_rgba_from_device_buffer()
                else:
                    raw = cam.get_rgba()
                if raw is not None and raw.size == (w * h * 4):
                    frame = raw.reshape((h, w, 4))[:, :, :3]
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8)
                    self.video_writer.write(frame)
        except KeyboardInterrupt:
            print("Interrupted, shutting down.")
        finally:
            self.video_writer.release()
            carb.log_warn("PegasusApp closing.")
            self.timeline.stop()
            simulation_app.close()

def main():
    app = PegasusApp()
    app.run()

if __name__ == "__main__":
    main()
