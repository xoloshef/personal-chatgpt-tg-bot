"""
Plugin manager with lazy loading - only loads plugins listed in PLUGINS env.
Set PLUGINS= to disable all plugins and avoid plugin dependencies.
"""
import importlib
import json

# Mapping: plugin name -> (module path, class name)
PLUGIN_REGISTRY = {
    'wolfram': ('plugins.wolfram_alpha', 'WolframAlphaPlugin'),
    'weather': ('plugins.weather', 'WeatherPlugin'),
    'crypto': ('plugins.crypto', 'CryptoPlugin'),
    'ddg_web_search': ('plugins.ddg_web_search', 'DDGWebSearchPlugin'),
    'ddg_image_search': ('plugins.ddg_image_search', 'DDGImageSearchPlugin'),
    'worldtimeapi': ('plugins.worldtimeapi', 'WorldTimeApiPlugin'),
    'youtube_audio_extractor': ('plugins.youtube_audio_extractor', 'YouTubeAudioExtractorPlugin'),
    'dice': ('plugins.dice', 'DicePlugin'),
    'deepl_translate': ('plugins.deepl', 'DeeplTranslatePlugin'),
    'whois': ('plugins.whois_', 'WhoisPlugin'),
    'webshot': ('plugins.webshot', 'WebshotPlugin'),
    'iplocation': ('plugins.iplocation', 'IpLocationPlugin'),
}


class PluginManager:
    """
    Manages plugins with lazy loading - only loads plugins that are enabled.
    """

    def __init__(self, config):
        enabled = [p.strip() for p in config.get('plugins', []) if p.strip()]
        self.plugins = []
        for name in enabled:
            if name in PLUGIN_REGISTRY:
                try:
                    module_path, class_name = PLUGIN_REGISTRY[name]
                    module = importlib.import_module(module_path)
                    plugin_class = getattr(module, class_name)
                    self.plugins.append(plugin_class())
                except Exception as e:
                    import logging
                    logging.warning(f'Failed to load plugin {name}: {e}')

    def get_functions_specs(self):
        specs = []
        for plugin in self.plugins:
            specs.extend(plugin.get_spec())
        return specs

    async def call_function(self, function_name, helper, arguments):
        plugin = self._get_plugin_by_function_name(function_name)
        if not plugin:
            return json.dumps({'error': f'Function {function_name} not found'})
        return json.dumps(await plugin.execute(function_name, helper, **json.loads(arguments)), default=str)

    def get_plugin_source_name(self, function_name) -> str:
        plugin = self._get_plugin_by_function_name(function_name)
        return plugin.get_source_name() if plugin else ''

    def _get_plugin_by_function_name(self, function_name):
        for plugin in self.plugins:
            if function_name in (s.get('name') for s in plugin.get_spec()):
                return plugin
        return None
