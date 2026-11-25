// Ported from Jl4cTuk/morphe-patches (GPL-3.0).
// Source: patches/src/main/kotlin/app/template/patches/ozon/reviews/Fingerprints.kt
// At commit: 8670317938ee76d0968fde57379ff57b52a79f69
// Modifications: package/namespace adapted to app.patchguard.
package app.patchguard.patches.ozon.reviews

import app.morphe.patcher.Fingerprint

/** Matches the mapper that creates the post-purchase rating bottom sheet. */
object RateItemsMapperFingerprint : Fingerprint(
    definingClass = "Lru/ozon/app/android/ugc/widgets/rateItemsV2/core/RateItemsV2Mapper;",
    name = "invoke",
    returnType = "Ljava/util/List;",
    parameters = listOf(
        "Lru/ozon/app/android/ugc/widgets/rateItemsV2/data/RateItemsV2Wrapper;",
        "L",
    ),
)
