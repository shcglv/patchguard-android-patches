// Ported from Jl4cTuk/morphe-patches (GPL-3.0).
// Source: patches/src/main/kotlin/app/template/patches/ozon/shared/Constants.kt
// At commit: 8670317938ee76d0968fde57379ff57b52a79f69
// Modifications: package/namespace adapted to app.patchguard. Compatibility is unchanged.
package app.patchguard.patches.ozon.shared

import app.morphe.patcher.patch.ApkFileType
import app.morphe.patcher.patch.AppTarget
import app.morphe.patcher.patch.Compatibility

internal object Constants {
    const val PACKAGE_NAME = "ru.ozon.app.android"

    val COMPATIBILITY_OZON_CURRENT = Compatibility(
        name = "Ozon",
        packageName = PACKAGE_NAME,
        apkFileType = ApkFileType.APK,
        appIconColor = 0x005BFF,
        targets = listOf(
            AppTarget(
                version = "19.31.0",
                versionCode = 2706,
                minSdk = 26,
            ),
        ),
    )
}
