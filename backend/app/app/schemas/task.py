from typing import Optional, Union, List, Dict
from ipaddress import IPv4Address, IPv6Address
from pydantic import BaseModel, Field


class Task(BaseModel):
    func: Optional[str] = Field(None, max_length=128)

class TaskArgs(BaseModel):
    args: Optional[List[Union[int,str]]]
    kwargs: Optional[Dict[str,Union[int,str]]]
    run_options: Optional[Dict[str,str]]