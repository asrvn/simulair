#line 1 "/builds/omniverse/usd-ci/USD/pxr/usdImaging/usdImagingGL/unitTestGLDrawing.h"
//
// Copyright 2016 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
#ifndef PXR_USD_IMAGING_USD_IMAGING_GL_UNIT_TEST_GLDRAWING_H
#define PXR_USD_IMAGING_USD_IMAGING_GL_UNIT_TEST_GLDRAWING_H

#include "pxr/pxr.h"
#include "pxr/base/gf/vec4d.h"
#include "pxr/base/vt/dictionary.h"

#include "pxr/base/tf/declarePtrs.h"

#include "pxr/usdImaging/usdImagingGL/engine.h"
#include "pxr/usdImaging/usdImaging/delegate.h"

#include <string>
#include <vector>

PXR_NAMESPACE_OPEN_SCOPE


class UsdImagingGL_UnitTestWindow;

/// \class UsdImagingGL_UnitTestGLDrawing
///
/// A helper class for unit tests which need to perform GL drawing.
///
class UsdImagingGL_UnitTestGLDrawing
{
public:
    UsdImagingGL_UnitTestGLDrawing();
    virtual ~UsdImagingGL_UnitTestGLDrawing();

    int GetWidth() const;
    int GetHeight() const;

    bool IsEnabledTestLighting() const { return _testLighting; }
    bool IsEnabledSceneLights() const { return _sceneLights; }
    bool IsEnabledCameraLight() const { return _cameraLight; }
    bool IsEnabledSceneMaterials() const { return _enableSceneMaterials; }
    bool IsEnabledUnloadedAsBounds() const { return _unloadedAsBounds; }
    
    bool IsShowGuides() const { return _showGuides; }
    bool IsShowRender() const { return _showRender; }
    bool IsShowProxy() const { return _showProxy; }

    // We use a client created presentation output (framebuffer) when
    // testing present output, otherwise we output AOV images directly.
    bool PresentComposite() const { return _presentComposite; }
    bool PresentDisabled() const { return _presentDisabled; }
    bool IsEnabledTestPresentOutput() const {
        return PresentComposite() || PresentDisabled();
    }

    UsdImagingGLDrawMode GetDrawMode() const { return _drawMode; }

    std::string const & GetStageFilePath() const { return _stageFilePath; }
    std::string const & GetOutputFilePath() const { return _outputFilePath; }

    std::string const & GetCameraPath() const { return _cameraPath; }
    std::vector<GfVec4d> const & GetClipPlanes() const { return _clipPlanes; }
    std::vector<double> const& GetTimes() const { return _times; }
    GfVec4f const & GetClearColor() const { return _clearColor; }
    GfVec3f const & GetTranslate() const { return _translate; }
    VtDictionary const &GetRenderSettings() const { return _renderSettings; }
    TfToken const & GetRendererAov() const { return _rendererAov; }
    std::string const &GetPerfStatsFile() const { return _perfStatsFile; }
    float GetPixelAspectRatio() const { return _pixelAspectRatio; }
    GfRange2f const & GetDisplayWindow() const { return _displayWindow; }
    GfRect2i const & GetDataWindow() const { return _dataWindow; }
    CameraUtilConformWindowPolicy const &
    GetWindowPolicy() const { return _windowPolicy; }
    UsdImagingGLCullStyle GetCullStyle() const { return _cullStyle; }

    void RunTest(int argc, char *argv[]);

    virtual void InitTest() = 0;
    virtual void DrawTest(bool offscreen) = 0;
    virtual void ShutdownTest() { }

    virtual void MousePress(int button, int x, int y, int modKeys);
    virtual void MouseRelease(int button, int x, int y, int modKeys);
    virtual void MouseMove(int x, int y, int modKeys);
    virtual void KeyRelease(int key);

    // Write an output image from the specified AOV or from the client
    // created presentation output when present output testing is enabled.
    bool WriteToFile(UsdImagingGLEngine *engine,
                     TfToken const &aovName,
                     std::string const &filename);

    // Helper method to write an output image from the specified AOV.
    static bool WriteAovToFile(UsdImagingGLEngine *engine,
                               TfToken const &aovName,
                               std::string const &filename);

protected:
    float _GetComplexity() const { return _complexity; }
    bool _ShouldFrameAll() const { return _shouldFrameAll; }
    TfToken _GetRenderer() const { return _renderer; }

    HdRenderIndex *_GetRenderIndex(UsdImagingGLEngine *engine) {
        return engine->_GetRenderIndex();
    }
    
    void _Render(UsdImagingGLEngine *engine, 
                 const UsdImagingGLRenderParams &params) {
        SdfPathVector roots(1, SdfPath::AbsoluteRootPath());
        engine->RenderBatch(roots, params);
    }

private:
    struct _Args;
    void _Parse(int argc, char *argv[], _Args* args);

private:
    UsdImagingGL_UnitTestWindow *_widget;
    bool _testLighting;
    bool _sceneLights;
    bool _cameraLight;
    std::string _cameraPath;
    bool _enableSceneMaterials;
    bool _unloadedAsBounds;

    std::string _stageFilePath;
    std::string _outputFilePath;

    float _complexity;
    TfToken _renderer;

    std::vector<double> _times;

    std::vector<GfVec4d> _clipPlanes;

    UsdImagingGLDrawMode _drawMode;
    bool _shouldFrameAll;
    UsdImagingGLCullStyle _cullStyle;
    GfVec4f _clearColor;
    GfVec3f _translate;
    float _pixelAspectRatio;
    GfRange2f _displayWindow;
    GfRect2i _dataWindow;
    CameraUtilConformWindowPolicy _windowPolicy;

    VtDictionary _renderSettings;
    TfToken _rendererAov;
    std::string _perfStatsFile;
    std::string _traceFile;

    bool _showGuides;
    bool _showRender;
    bool _showProxy;
    bool _presentComposite;
    bool _presentDisabled;
};


PXR_NAMESPACE_CLOSE_SCOPE

#endif // PXR_USD_IMAGING_USD_IMAGING_GL_UNIT_TEST_GLDRAWING_H
