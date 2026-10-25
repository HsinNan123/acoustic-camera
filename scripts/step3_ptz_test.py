"""Step 3a: can Python turn the Tapo C545D telephoto lens over ONVIF?

Lists the camera's video profiles and which PTZ moves it accepts, then (with --move)
turns the lens a little right, measures how far and how fast, and turns it back.

Needs `.env` in the project folder (never committed, never printed):
    TAPO_HOST=192.168.x.x
    TAPO_USER=<Camera Account user name from the Tapo app>
    TAPO_PASS=<Camera Account password>
    TAPO_ONVIF_PORT=2020        (optional; Tapo cameras use 2020)

Run from the project folder:
    .venv\\Scripts\\python scripts\\step3_ptz_test.py          (read only, nothing moves)
    .venv\\Scripts\\python scripts\\step3_ptz_test.py --move   (turns the lens and back)
"""
import argparse
import sys
import time
from pathlib import Path

from onvif import ONVIFCamera

ENV = Path(__file__).resolve().parents[1] / ".env"
STEP = 0.1  # ONVIF pan units; how many degrees this is, is what the test finds out


def read_env():
    if not ENV.exists():
        sys.exit(f"Missing {ENV}. Create it with TAPO_HOST, TAPO_USER, TAPO_PASS.")
    env = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    missing = [k for k in ("TAPO_HOST", "TAPO_USER", "TAPO_PASS") if not env.get(k)]
    if missing:
        sys.exit(f"{ENV} lacks: {', '.join(missing)}")
    return env


def position(ptz, token):
    pos = ptz.GetStatus({"ProfileToken": token}).Position
    return (pos.PanTilt.x, pos.PanTilt.y) if pos and pos.PanTilt else None


def wait_until_still(ptz, token, timeout=10.0):
    """Poll the position until it stops changing; return (seconds, final position)."""
    start, last = time.time(), position(ptz, token)
    while time.time() - start < timeout:
        time.sleep(0.2)
        now = position(ptz, token)
        if now == last and time.time() - start > 0.6:
            return time.time() - start, now
        last = now
    return timeout, last


def try_move(name, call):
    try:
        call()
        return True
    except Exception as e:  # report every refusal; that is the point of the test
        print(f"  {name}: refused ({type(e).__name__}: {str(e)[:120]})")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--move", action="store_true", help="turn the lens and back")
    args = parser.parse_args()
    env = read_env()

    cam = ONVIFCamera(env["TAPO_HOST"], int(env.get("TAPO_ONVIF_PORT", 2020)),
                      env["TAPO_USER"], env["TAPO_PASS"])
    info = cam.devicemgmt.GetDeviceInformation()
    print(f"Camera: {info.Manufacturer} {info.Model}, firmware {info.FirmwareVersion}")

    media, ptz = cam.create_media_service(), cam.create_ptz_service()
    ptz_profiles = []
    for p in media.GetProfiles():
        res = p.VideoEncoderConfiguration.Resolution if p.VideoEncoderConfiguration else None
        size = f"{res.Width}x{res.Height}" if res else "?"
        has_ptz = p.PTZConfiguration is not None
        print(f"Profile {p.token} ({p.Name}): {size}, PTZ {'yes' if has_ptz else 'no'}")
        if has_ptz:
            ptz_profiles.append(p)
    if not ptz_profiles:
        sys.exit("No profile has PTZ: ONVIF cannot move this camera. Next: try pytapo.")

    profile = ptz_profiles[0]
    token = profile.token
    opts = ptz.GetConfigurationOptions({"ConfigurationToken": profile.PTZConfiguration.token})
    spaces = opts.Spaces
    for kind in ("AbsolutePanTiltPositionSpace", "RelativePanTiltTranslationSpace",
                 "ContinuousPanTiltVelocitySpace"):
        found = getattr(spaces, kind, None) or []
        for s in found:
            print(f"{kind}: x {s.XRange.Min}..{s.XRange.Max}, y {s.YRange.Min}..{s.YRange.Max}")
        if not found:
            print(f"{kind}: not offered")
    presets = ptz.GetPresets({"ProfileToken": token}) or []
    print(f"Presets: {len(presets)}")
    start = position(ptz, token)
    print(f"Position now: {start}")

    if not args.move:
        print("Read-only run done. Add --move to turn the lens.")
        return

    print(f"\nRelativeMove pan +{STEP}:")
    if try_move("RelativeMove", lambda: ptz.RelativeMove(
            {"ProfileToken": token, "Translation": {"PanTilt": {"x": STEP, "y": 0}}})):
        secs, end = wait_until_still(ptz, token)
        print(f"  moved from {start} to {end} in {secs:.1f} s")
        try_move("RelativeMove back", lambda: ptz.RelativeMove(
            {"ProfileToken": token, "Translation": {"PanTilt": {"x": -STEP, "y": 0}}}))
        wait_until_still(ptz, token)

    if start is not None:
        print(f"\nAbsoluteMove to pan {start[0] + STEP:.3f}:")
        if try_move("AbsoluteMove", lambda: ptz.AbsoluteMove(
                {"ProfileToken": token, "Position": {"PanTilt": {"x": start[0] + STEP, "y": start[1]}}})):
            secs, end = wait_until_still(ptz, token)
            print(f"  moved from {start} to {end} in {secs:.1f} s")
            try_move("AbsoluteMove back", lambda: ptz.AbsoluteMove(
                {"ProfileToken": token, "Position": {"PanTilt": {"x": start[0], "y": start[1]}}}))
            wait_until_still(ptz, token)

    print("\nContinuousMove right for 1 s:")
    if try_move("ContinuousMove", lambda: ptz.ContinuousMove(
            {"ProfileToken": token, "Velocity": {"PanTilt": {"x": 0.5, "y": 0}}})):
        time.sleep(1.0)
        ptz.Stop({"ProfileToken": token, "PanTilt": True})
        secs, end = wait_until_still(ptz, token)
        print(f"  moved from {start} to {end}; settled {secs:.1f} s after Stop")
        ptz.ContinuousMove({"ProfileToken": token, "Velocity": {"PanTilt": {"x": -0.5, "y": 0}}})
        time.sleep(1.0)
        ptz.Stop({"ProfileToken": token, "PanTilt": True})
        wait_until_still(ptz, token)

    print(f"\nPosition at the end: {position(ptz, token)} (start {start})")
    print("Next: compare the picture with the start. How many degrees did one move turn?")


if __name__ == "__main__":
    main()
