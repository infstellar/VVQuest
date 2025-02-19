import os
from typing import Dict, List, Optional
from confz import BaseConfig, ConfigSource, FileSource
from pydantic import Field

class EmbeddingModelConfig(BaseConfig):
    name: str
    performance: str

class ModelsConfig(BaseConfig):
    embedding_models: Dict[str, EmbeddingModelConfig]
    default_model: str

class PathsConfig(BaseConfig):
    image_dirs: Dict
    cache_file: str
    models_dir: str
    api_embeddings_cache_file: str

class ApiConfig(BaseConfig):
    silicon_api_key: Optional[str] = None

class MiscConfig(BaseConfig):
    adapt_for_old_version: bool

class Config(BaseConfig):
    api: ApiConfig
    models: ModelsConfig
    paths: PathsConfig
    misc: MiscConfig

    CONFIG_SOURCES = [
        FileSource(
            file='config/config.yaml'
        ),
    ]

    @property
    def base_dir(self) -> str:
        """获取项目根目录"""
        return os.path.dirname(os.path.dirname(__file__))

    def get_model_path(self, model_name: str) -> str:
        """获取模型保存路径"""
        return os.path.join(self.base_dir, self.paths.models_dir, model_name.replace('/', '_'))

    def get_absolute_image_dirs(self) -> List[str]:
        """获取图片目录的绝对路径"""
        return [v['path'] for v in self.paths.image_dirs.values()]

    def get_absolute_cache_file(self) -> str:
        """获取缓存文件的绝对路径"""
        return os.path.join(self.base_dir, self.paths.cache_file)

    def get_abs_api_cache_file(self) -> str:
        """获取缓存文件的绝对路径"""
        return os.path.join(self.base_dir, self.paths.api_embeddings_cache_file)

    def reload(self) -> None:
        """重新加载配置文件"""
        new_config = Config()
        self.api = new_config.api
        self.models = new_config.models
        self.paths = new_config.paths
        self.misc = new_config.misc

# 创建全局配置实例
config = Config()

def reload_config() -> None:
    """重新加载配置文件"""
    global config
    config = Config()