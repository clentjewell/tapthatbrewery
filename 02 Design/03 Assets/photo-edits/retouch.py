import cv2, numpy as np
im = cv2.imread('founder-tap-wall_original.jpg').astype(np.float32)
H, W = im.shape[:2]
out = im.copy()

# ---------- 1. Face: skin mask, de-shine, even tone ----------
lab = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
ycc = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2YCrCb)
skin = cv2.inRange(ycc, (40, 135, 85), (255, 180, 130))
region = np.zeros((H, W), np.uint8)
cv2.ellipse(region, (468, 318), (112, 135), 0, 0, 360, 255, -1)
region[:228] = 0                                  # stay under the cap brim
region[:238, :400] = 0
# keep eyes, brows and lips out of the smoothing
for c, ax in [((446, 247), (22, 9)), ((523, 247), (20, 9)), ((486, 342), (48, 13))]:
    cv2.ellipse(region, c, ax, 0, 0, 360, 0, -1)
mask = cv2.bitwise_and(skin, region)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
m = 0.85 * cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), 9)[..., None]

L, A, B = cv2.split(lab)
# frequency separation: smooth the low-frequency tone, keep most texture
low = cv2.bilateralFilter(im.astype(np.uint8), 9, 30, 9).astype(np.float32)
low = cv2.GaussianBlur(low, (0, 0), 2.2)
high = im - cv2.GaussianBlur(im, (0, 0), 2.2)
smooth = low + 0.75 * high
slab = cv2.cvtColor(np.clip(smooth, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
sL, sA, sB = cv2.split(slab)
# de-shine: pull highlights above the local base down
base = cv2.GaussianBlur(sL, (0, 0), 14)
hi = np.clip(sL - base - 4, 0, None)
sL = sL - 0.45 * hi + 1.0
# even skin tone: calm blotchy redness, pull a/b toward their local average
sA = sA - 0.3 * (sA - cv2.GaussianBlur(sA, (0, 0), 10)) + 0.8
sB = sB - 0.2 * (sB - cv2.GaussianBlur(sB, (0, 0), 10)) + 2.0
fixed = cv2.cvtColor(cv2.merge([np.clip(x, 0, 255) for x in (sL, sA, sB)]).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
out = out * (1 - m) + fixed * m

# ---------- 2. Cap: official badge warped onto the patch ----------
logo = cv2.imread('../../01 Inputs/brand/TapThat_Primary-Badge_on-grey_202x132.png').astype(np.float32)
bg = logo[2, 2]
d = np.abs(logo - bg).sum(2)
alpha = np.clip((d - 25) / 40, 0, 1)
alpha = cv2.erode(alpha, np.ones((2, 2), np.uint8))
# pop: a little more contrast and saturation on the artwork
hsv = cv2.cvtColor(logo.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
hsv[..., 1] = np.clip(hsv[..., 1] * 1.15, 0, 255)
logo = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
logo = np.clip((logo - 128) * 1.08 + 128, 0, 255)

S = 4  # upsample before warping for cleaner edges
logoU = cv2.resize(logo, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
alphaU = cv2.resize(alpha, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
sp = {'P': (101, 11), 'UL': (20, 40), 'LL': (25, 106), 'B': (101, 122), 'LR': (178, 106), 'UR': (184, 40), 'C': (101, 70)}
dp = {'P': (468, 82.5), 'UL': (405.5, 119.5), 'LL': (412, 148.5), 'B': (475, 144.5), 'LR': (538.5, 139.5), 'UR': (527.5, 111), 'C': (472, 118)}
ring = ['P', 'UR', 'LR', 'B', 'LL', 'UL']
wl = np.zeros_like(im); wa = np.zeros((H, W), np.float32)
for i in range(6):
    k = [ring[i], ring[(i + 1) % 6], 'C']
    s3 = np.float32([sp[x] for x in k]) * S
    d3 = np.float32([dp[x] for x in k])
    M = cv2.getAffineTransform(s3, d3)
    tri = np.zeros((H, W), np.uint8)
    cv2.fillConvexPoly(tri, np.int32(np.round(d3 * 8)), 255, shift=3)
    tri = cv2.dilate(tri, np.ones((2, 2), np.uint8)) > 0
    tl = cv2.warpAffine(logoU, M, (W, H), flags=cv2.INTER_AREA)
    ta = cv2.warpAffine(alphaU, M, (W, H), flags=cv2.INTER_LINEAR)
    wl[tri] = tl[tri]; wa[tri] = ta[tri]
# brim sits in front of the patch at bottom-right
occ = np.zeros((H, W), np.uint8)
brim = np.int32([[470, 150], [478, 143.3], [488, 136.3], [503, 133.8], [528, 134.2], [550, 136.7], [560, 160], [470, 160]])
cv2.fillPoly(occ, [brim], 255)
occ = cv2.GaussianBlur(occ.astype(np.float32) / 255, (0, 0), 0.8)
wa = wa * (1 - occ)
# match the photo: slight softness, cap's own shading, grain
wl = cv2.GaussianBlur(wl, (0, 0), 0.55)
shade = cv2.GaussianBlur(cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 12)
ref = shade[95:140, 420:530].mean()
wl = wl * np.clip((shade / ref) ** 0.25, 0.85, 1.1)[..., None]
wl += np.random.default_rng(1).normal(0, 2.5, wl.shape)
wa = cv2.GaussianBlur(wa, (0, 0), 0.5)[..., None]
out = out * (1 - wa) + wl * wa

out = np.clip(out, 0, 255).astype(np.uint8)
cv2.imwrite('founder-tap-wall_retouched.jpg', out, [cv2.IMWRITE_JPEG_QUALITY, 95])
