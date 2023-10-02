# Copyright The Caikit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import alog
from caikit.core import TaskBase, task
from caikit.core.toolkit.errors import error_handler
from caikit_embeddings.data_model.reranker import RerankPrediction, RerankDocuments

from typing import List

logger = alog.use_channel("<SMPL_BLK>")
error = error_handler.get(logger)

@task(
    required_parameters={
        "queries": List[str],
        "documents": RerankDocuments,
        "top_n": int,
    },
    output_type=RerankPrediction,
)
class RerankTask(TaskBase):
    pass