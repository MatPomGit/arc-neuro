"""Reference geometry for synthetic examples and frozen E01 measurement units."""
from math import atan2, degrees, hypot, isfinite


def errors(target, estimate, mm_per_pixel, eye_projection, distance_mm):
    """Return planar pixel error and full angle between rays from the eye."""
    coordinates = (*target, *estimate, *mm_per_pixel, *eye_projection, distance_mm)
    if not all(map(isfinite, coordinates)) or min(*mm_per_pixel, distance_mm) <= 0:
        raise ValueError("finite coordinates and positive screen scales and distance required")
    rays = [
        ((point[0] - eye_projection[0]) * mm_per_pixel[0],
         (point[1] - eye_projection[1]) * mm_per_pixel[1], distance_mm)
        for point in (target, estimate)
    ]
    (a, b, c), (d, e, f) = rays
    cross = (b * f - c * e, c * d - a * f, a * e - b * d)
    dot = a * d + b * e + c * f
    return hypot(estimate[0] - target[0], estimate[1] - target[1]), degrees(atan2(hypot(*cross), dot))


if __name__ == "__main__":
    print("case,error_px,error_deg")
    for label, x in (("center", 0), ("off_axis", 500)):
        pixel, angular = errors((x, 0), (x + 100, 0), (0.1, 0.1), (0, 0), 400)
        print(f"{label},{pixel:.6f},{angular:.6f}")
