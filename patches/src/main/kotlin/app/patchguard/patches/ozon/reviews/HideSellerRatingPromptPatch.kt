// Ported from Jl4cTuk/morphe-patches (GPL-3.0).
// Source: patches/src/main/kotlin/app/template/patches/ozon/reviews/HideSellerRatingPromptPatch.kt
// At commit: 8670317938ee76d0968fde57379ff57b52a79f69
// Modifications: package/namespace adapted to app.patchguard. Behaviour is unchanged.
package app.patchguard.patches.ozon.reviews

import app.morphe.patcher.extensions.InstructionExtensions.addInstructions
import app.morphe.patcher.patch.bytecodePatch
import app.patchguard.patches.ozon.shared.Constants.COMPATIBILITY_OZON_CURRENT

@Suppress("unused")
val hideSellerRatingPromptPatch = bytecodePatch(
    name = "Hide seller rating prompt",
    description = "Removes the post-purchase seller rating prompt.",
    default = true,
) {
    compatibleWith(COMPATIBILITY_OZON_CURRENT)

    execute {
        RateItemsMapperFingerprint.method.addInstructions(
            0,
            """
                invoke-static {}, Ljava/util/Collections;->emptyList()Ljava/util/List;
                move-result-object v0
                return-object v0
            """.trimIndent(),
        )
    }
}
