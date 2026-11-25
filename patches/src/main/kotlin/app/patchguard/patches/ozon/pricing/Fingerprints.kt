// Ported from Jl4cTuk/morphe-patches (GPL-3.0).
// Source: patches/src/main/kotlin/app/template/patches/ozon/pricing/Fingerprints.kt
// At commit: 8670317938ee76d0968fde57379ff57b52a79f69
// Modifications: package/namespace adapted to app.patchguard.
package app.patchguard.patches.ozon.pricing

import app.morphe.patcher.Fingerprint

/** Matches the text getter for an individual component of an Ozon price atom. */
object PriceComponentTextFingerprint : Fingerprint(
    definingClass = "Lru/ozon/uni/atoms/data/price/PriceDTO\$Component;",
    name = "getText",
    returnType = "Ljava/lang/String;",
    parameters = emptyList(),
)

/** Matches the separate discount label rendered next to an Ozon price atom. */
object PriceDiscountFingerprint : Fingerprint(
    definingClass = "Lru/ozon/uni/atoms/data/price/PriceDTO;",
    name = "getDiscount",
    returnType = "Ljava/lang/String;",
    parameters = emptyList(),
)

/** Matches the checkout-composer total view holder shared by the cart and checkout pages. */
object CartTotalBindFingerprint : Fingerprint(
    definingClass = "Lru/ozon/app/android/checkoutcomposer/total/presentation/main/TotalVH;",
    name = "bind",
    returnType = "V",
    parameters = listOf(
        "Lru/ozon/app/android/checkoutcomposer/total/models/TotalVO;",
        "L",
    ),
)
