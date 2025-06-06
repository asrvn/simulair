#line 1 "/builds/omniverse/usd-ci/USD/pxr/imaging/hgiGL/shaderSection.h"
//
// Copyright 2020 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//

#ifndef PXR_IMAGING_HGIGL_SHADERSECTION_H
#define PXR_IMAGING_HGIGL_SHADERSECTION_H

#include "pxr/imaging/hgi/shaderFunctionDesc.h"
#include "pxr/imaging/hgi/shaderSection.h"
#include "pxr/imaging/hgiGL/api.h"

#include <string>
#include <vector>

PXR_NAMESPACE_OPEN_SCOPE

/// \class HgiGLShaderSection
///
/// Base class for OpenGL code sections. The generator holds these
///
class HgiGLShaderSection : public HgiShaderSection
{
public:
    HGIGL_API
    explicit HgiGLShaderSection(
        const std::string &identifier,
        const HgiShaderSectionAttributeVector &attributes = {},
        const std::string &storageQualifier = std::string(),
        const std::string &defaultValue = std::string(),
        const std::string &arraySize = std::string(),
        const std::string &blockInstanceIdentifier = std::string());

    HGIGL_API
    ~HgiGLShaderSection() override;

    HGIGL_API
    void WriteDeclaration(std::ostream &ss) const override;
    HGIGL_API
    void WriteParameter(std::ostream &ss) const override;

    HGIGL_API
    virtual bool VisitGlobalIncludes(std::ostream &ss);
    HGIGL_API
    virtual bool VisitGlobalMacros(std::ostream &ss);
    HGIGL_API
    virtual bool VisitGlobalStructs(std::ostream &ss);
    HGIGL_API
    virtual bool VisitGlobalMemberDeclarations(std::ostream &ss);
    HGIGL_API
    virtual bool VisitGlobalFunctionDefinitions(std::ostream &ss);

private:
    HgiGLShaderSection() = delete;
    HgiGLShaderSection & operator=(const HgiGLShaderSection&) = delete;
    HgiGLShaderSection(const HgiGLShaderSection&) = delete;

    const std::string _storageQualifier;
    const std::string _arraySize;
};

using HgiGLShaderSectionPtrVector = 
    std::vector<HgiGLShaderSection*>;

/// \class HgiGLMacroShaderSection
///
/// A ShaderSection for defining macros.
/// Accepts raw strings and dumps it to the global scope under includes
///
class HgiGLMacroShaderSection final: public HgiGLShaderSection
{
public:
    HGIGL_API
    explicit HgiGLMacroShaderSection(
        const std::string &macroDeclaration,
        const std::string &macroComment);

    HGIGL_API
    ~HgiGLMacroShaderSection() override;

    HGIGL_API
    bool VisitGlobalMacros(std::ostream &ss) override;

private:
    HgiGLMacroShaderSection() = delete;
    HgiGLMacroShaderSection & operator=(
        const HgiGLMacroShaderSection&) = delete;
    HgiGLMacroShaderSection(const HgiGLMacroShaderSection&) = delete;

    const std::string _macroComment;
};

/// \class HgiGLMemberShaderSection
///
/// Declares a member in global scope, for declaring instances of structs, constant
/// params etc - it's quite flexible in it's writing capabilities
///
class HgiGLMemberShaderSection final: public HgiGLShaderSection
{
public:
    HGIGL_API
    explicit HgiGLMemberShaderSection(
        const std::string &identifier,
        const std::string &typeName,
        const HgiInterpolationType interpolation,
        const HgiSamplingType sampling,
        const HgiStorageType storage,
        const HgiShaderSectionAttributeVector &attributes,
        const std::string &storageQualifier = std::string(),
        const std::string &defaultValue = std::string(),
        const std::string &arraySize = std::string(),
        const std::string &blockInstanceIdentifier = std::string());

    HGIGL_API
    ~HgiGLMemberShaderSection() override;

    HGIGL_API
    bool VisitGlobalMemberDeclarations(std::ostream &ss) override;

    HGIGL_API
    void WriteType(std::ostream& ss) const override;

    HGIGL_API
    void WriteInterpolation(std::ostream& ss) const;
    
    HGIGL_API
    void WriteSampling(std::ostream& ss) const;
    
    HGIGL_API
    void WriteStorage(std::ostream& ss) const;

private:
    HgiGLMemberShaderSection() = delete;
    HgiGLMemberShaderSection & operator=(
        const HgiGLMemberShaderSection&) = delete;
    HgiGLMemberShaderSection(const HgiGLMemberShaderSection&) = delete;

    std::string _typeName;
    HgiInterpolationType _interpolation;
    HgiSamplingType _sampling;
    HgiStorageType _storage;
};

using HgiGLMemberShaderSectionPtrVector = 
    std::vector<HgiGLMemberShaderSection*>;

/// \class HgiGLBlockShaderSection
///
/// For writing out uniform blocks, defines them in the global member declerations.
///
class HgiGLBlockShaderSection final: public HgiGLShaderSection
{
public:
    HGIGL_API
    explicit HgiGLBlockShaderSection(
            const std::string &identifier,
            const HgiShaderFunctionParamDescVector &parameters,
            const uint32_t bindingNo=0);

    HGIGL_API
    ~HgiGLBlockShaderSection() override;

    HGIGL_API
    bool VisitGlobalMemberDeclarations(std::ostream &ss) override;

private:
    const HgiShaderFunctionParamDescVector _parameters;
    const uint32_t _bindingNo;
};

/// \class HgiGLTextureShaderSection
///
/// Declares OpenGL textures, and their cross language function
///
class HgiGLTextureShaderSection final: public HgiGLShaderSection
{
public:
    HGIGL_API
    explicit HgiGLTextureShaderSection(
        const std::string &identifier,
        const uint32_t layoutIndex,
        const uint32_t dimensions,
        const HgiFormat format,
        const HgiShaderTextureType textureType,
        const uint32_t arraySize,
        const bool writable,
        const HgiShaderSectionAttributeVector &attributes,
        const std::string &defaultValue = std::string());

    HGIGL_API
    ~HgiGLTextureShaderSection() override;

    HGIGL_API
    void WriteType(std::ostream &ss) const override;

    HGIGL_API
    bool VisitGlobalMemberDeclarations(std::ostream &ss) override;
    HGIGL_API
    bool VisitGlobalFunctionDefinitions(std::ostream &ss) override;

private:
    HgiGLTextureShaderSection() = delete;
    HgiGLTextureShaderSection & operator=(
        const HgiGLTextureShaderSection&) = delete;
    HgiGLTextureShaderSection(const HgiGLTextureShaderSection&) = delete;
    
    void _WriteSamplerType(std::ostream &ss) const;
    void _WriteSampledDataType(std::ostream &ss) const;

    const uint32_t _dimensions;
    const HgiFormat _format;
    const HgiShaderTextureType _textureType;
    const uint32_t _arraySize;
    const bool _writable;
    static const std::string _storageQualifier;
};

/// \class HgiGLBufferShaderSection
///
/// Declares OpenGL buffers, and their cross language function
///
class HgiGLBufferShaderSection final: public HgiGLShaderSection
{
public:
    HGIGL_API
    explicit HgiGLBufferShaderSection(
        const std::string &identifier,
        const uint32_t layoutIndex,
        const std::string &type,
        const HgiBindingType binding,
        const std::string arraySize,
        const HgiShaderSectionAttributeVector &attributes);

    HGIGL_API
    ~HgiGLBufferShaderSection() override;

    HGIGL_API
    void WriteType(std::ostream &ss) const override;

    HGIGL_API
    bool VisitGlobalMemberDeclarations(std::ostream &ss) override;

private:
    HgiGLBufferShaderSection() = delete;
    HgiGLBufferShaderSection & operator=(
        const HgiGLBufferShaderSection&) = delete;
    HgiGLBufferShaderSection(const HgiGLBufferShaderSection&) = delete;

    const std::string _type;
    const HgiBindingType _binding;
    const std::string _arraySize;
};

/// \class HgiGLKeywordShaderSection
///
/// Declares reserved OpenGL shader inputs, and their cross language function
///
class HgiGLKeywordShaderSection final: public HgiGLShaderSection
{
public:
    HGIGL_API
    explicit HgiGLKeywordShaderSection(
        const std::string &identifier,
        const std::string &type,
        const std::string &glKeyword);

    HGIGL_API
    ~HgiGLKeywordShaderSection() override;

    HGIGL_API
    void WriteType(std::ostream &ss) const override;

    HGIGL_API
    bool VisitGlobalMemberDeclarations(std::ostream &ss) override;

private:
    HgiGLKeywordShaderSection() = delete;
    HgiGLKeywordShaderSection & operator=(
        const HgiGLKeywordShaderSection&) = delete;
    HgiGLKeywordShaderSection(const HgiGLKeywordShaderSection&) = delete;

    const std::string _type;
    const std::string _keyword;
};

/// \class HgiGLInterstageBlockShaderSection
///
/// Defines and writes out an interstage interface block
///
class HgiGLInterstageBlockShaderSection final: public HgiGLShaderSection
{
public:
    HGIGL_API
    explicit HgiGLInterstageBlockShaderSection(
        const std::string &blockIdentifier,
        const std::string &blockInstanceIdentifier,
        const std::string &qualifier,
        const std::string &arraySize,
        const HgiGLMemberShaderSectionPtrVector &members);

    HGIGL_API
    bool VisitGlobalMemberDeclarations(std::ostream &ss) override;

private:
    HgiGLInterstageBlockShaderSection() = delete;
    HgiGLInterstageBlockShaderSection & operator=(
        const HgiGLInterstageBlockShaderSection&) = delete;
    HgiGLInterstageBlockShaderSection(const HgiGLInterstageBlockShaderSection&) = delete;

    const std::string _qualifier;
    const HgiGLMemberShaderSectionPtrVector _members;
};

PXR_NAMESPACE_CLOSE_SCOPE

#endif
