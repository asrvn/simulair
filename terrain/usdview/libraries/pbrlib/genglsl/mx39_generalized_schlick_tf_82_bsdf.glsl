#include "lib/mx39_microfacet_specular.glsl"

void mx39_generalized_schlick_tf_82_bsdf_reflection(vec3 L, vec3 V, vec3 P, float occlusion, float weight, vec3 color0, vec3 color82, vec3 color90, float exponent, vec2 roughness, float thinfilm_thickness, float thinfilm_ior, vec3 N, vec3 X, int distribution, int scatter_mode, inout BSDF bsdf)
{
    if (weight < M_FLOAT_EPS)
    {
        return;
    }

    N = mx_forward_facing_normal(N, V);

    X = normalize(X - dot(X, N) * N);
    vec3 Y = cross(N, X);
    vec3 H = normalize(L + V);

    float NdotL = clamp(dot(N, L), M_FLOAT_EPS, 1.0);
    float NdotV = clamp(dot(N, V), M_FLOAT_EPS, 1.0);
    float VdotH = clamp(dot(V, H), M_FLOAT_EPS, 1.0);

    vec2 safeAlpha = clamp(roughness, M_FLOAT_EPS, 1.0);
    float avgAlpha = mx_average_alpha(safeAlpha);
    vec3 Ht = vec3(dot(H, X), dot(H, Y), dot(H, N));

    vec3 safeColor0 = max(color0, 0.0);
    vec3 safeColor82 = max(color82, 0.0);
    vec3 safeColor90 = max(color90, 0.0);
    Mx39FresnelData fd = mx39_init_fresnel_schlick(safeColor0, safeColor82, safeColor90, exponent, thinfilm_thickness, thinfilm_ior);
    vec3  F = mx39_compute_fresnel(VdotH, fd);
    float D = mx_ggx_NDF(Ht, safeAlpha);
    float G = mx_ggx_smith_G2(NdotL, NdotV, avgAlpha);

    vec3 comp = mx_ggx_energy_compensation(NdotV, avgAlpha, F);
    vec3 dirAlbedo = mx_ggx_dir_albedo(NdotV, avgAlpha, safeColor0, safeColor90) * comp;
    float avgDirAlbedo = dot(dirAlbedo, vec3(1.0 / 3.0));
    bsdf.throughput = vec3(1.0 - avgDirAlbedo * weight);

    // Note: NdotL is cancelled out
    bsdf.response = D * F * G * comp * occlusion * weight / (4.0 * NdotV);
}

void mx39_generalized_schlick_tf_82_bsdf_transmission(vec3 V, float weight, vec3 color0, vec3 color82, vec3 color90, float exponent, vec2 roughness, float thinfilm_thickness, float thinfilm_ior, vec3 N, vec3 X, int distribution, int scatter_mode, inout BSDF bsdf)
{
    if (weight < M_FLOAT_EPS)
    {
        return;
    }

    N = mx_forward_facing_normal(N, V);
    float NdotV = clamp(dot(N, V), M_FLOAT_EPS, 1.0);

    vec3 safeColor0 = max(color0, 0.0);
    vec3 safeColor82 = max(color82, 0.0);
    vec3 safeColor90 = max(color90, 0.0);
    Mx39FresnelData fd = mx39_init_fresnel_schlick(safeColor0, safeColor82, safeColor90, exponent, thinfilm_thickness, thinfilm_ior);
    vec3 F = mx39_compute_fresnel(NdotV, fd);

    vec2 safeAlpha = clamp(roughness, M_FLOAT_EPS, 1.0);
    float avgAlpha = mx_average_alpha(safeAlpha);

    vec3 comp = mx_ggx_energy_compensation(NdotV, avgAlpha, F);
    vec3 dirAlbedo = mx_ggx_dir_albedo(NdotV, avgAlpha, safeColor0, safeColor90) * comp;
    float avgDirAlbedo = dot(dirAlbedo, vec3(1.0 / 3.0));
    bsdf.throughput = vec3(1.0 - avgDirAlbedo * weight);

    if (scatter_mode != 0)
    {
        float avgF0 = dot(safeColor0, vec3(1.0 / 3.0));
        fd.ior = vec3(mx39_f0_to_ior(avgF0));
        bsdf.response = mx39_surface_transmission(N, V, X, safeAlpha, distribution, fd, safeColor0) * weight;
    }
}

void mx39_generalized_schlick_tf_82_bsdf_indirect(vec3 V, float weight, vec3 color0, vec3 color82, vec3 color90, float exponent, vec2 roughness, float thinfilm_thickness, float thinfilm_ior, vec3 N, vec3 X, int distribution, int scatter_mode, inout BSDF bsdf)
{
    if (weight < M_FLOAT_EPS)
    {
        return;
    }

    N = mx_forward_facing_normal(N, V);
    float NdotV = clamp(dot(N, V), M_FLOAT_EPS, 1.0);

    vec3 safeColor0 = max(color0, 0.0);
    vec3 safeColor82 = max(color82, 0.0);
    vec3 safeColor90 = max(color90, 0.0);
    Mx39FresnelData fd = mx39_init_fresnel_schlick(safeColor0, safeColor82, safeColor90, exponent, thinfilm_thickness, thinfilm_ior);
    vec3 F = mx39_compute_fresnel(NdotV, fd);

    vec2 safeAlpha = clamp(roughness, M_FLOAT_EPS, 1.0);
    float avgAlpha = mx_average_alpha(safeAlpha);
    vec3 comp = mx_ggx_energy_compensation(NdotV, avgAlpha, F);
    vec3 dirAlbedo = mx_ggx_dir_albedo(NdotV, avgAlpha, safeColor0, safeColor90) * comp;
    float avgDirAlbedo = dot(dirAlbedo, vec3(1.0 / 3.0));
    bsdf.throughput = vec3(1.0 - avgDirAlbedo * weight);

    vec3 Li = mx39_environment_radiance(N, V, X, safeAlpha, distribution, fd);
    bsdf.response = Li * comp * weight;
}
