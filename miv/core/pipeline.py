from typing import List, Optional, Union

import pathlib

from miv.core.operator.chainable import _Chainable
from miv.core.policy import _Runnable


class Pipeline:
    def __init__(self, node: _Chainable):
        self.execution_order: List[_Runnable] = node.topological_sort()

    def run(
        self,
        save_path: Optional[Union[str, pathlib.Path]] = "./results",
        no_cache: bool = False,
        dry_run: bool = False,
        verbose: bool = False,  # Use logging
    ):
        for node in self.execution_order:
            if verbose:
                print("Running: ", node)
            if hasattr(node, "cacher"):
                node.cacher.cache_policy = "OFF" if no_cache else "AUTO"
            node.run(dry_run=dry_run, save_path=save_path)
        if verbose:
            print("Pipeline done:")
            self.summarize()
            print("-"*46)

    def summarize(self):
        strs = []
        strs.append("Execution order:")
        for i, op in enumerate(self.execution_order):
            strs.append(f"{i}: {op}")
        return "\n".join(strs)
