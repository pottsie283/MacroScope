import importlib
import os

def test_sample_plugin():
    mod = importlib.import_module("macroscope.plugins.sample_plugin")
    plugin_class = getattr(mod, [c for c in dir(mod) if c.endswith("Plugin")][0])
    plugin = plugin_class()
    result = plugin.run(__file__)
    assert isinstance(result, dict)
    assert result.get("plugin") == "sample"
