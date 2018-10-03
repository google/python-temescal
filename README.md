Python control for LG speaker systems
=====================================

A simple Python API for controlling speakers from LG that can otherwise be controlled via the LG wifi speaker app.

Example use
-----------
Device discovery is out of scope of this project. Use an mdns module such as netdisco to locate devices on your network.

Connect to a speaker at 192.168.1.15

```
import temescal

speaker = temescal.temescal("192.168.1.15")
```

Connect with a registered callback:

```
import temescal

speaker = temescal.temescal("192.168.1.15", callback=speaker_callback)
```

The callback will be called whenever Temescal receives a packet from the speaker. This may be a response to a sent command or a gratuitous status update triggered by another control event.

Get the current equaliser state:
```
import temescal

speaker = temescal.temescal("192.168.1.15", callback=speaker_callback)
speaker.get_eq()
```

The callback routine will be called with the response.

Set the volume to 20:
```
import temescal

speaker = temescal.temescal("192.168.1.15", callback=speaker_callback)
speaker.set_volume(20)
```

This is not an officially supported Google project.