import json
import requests
import os #获取当前目录路径
import xlwt
import time
header = {
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhMmZiNjI1MC0wZDQzLTAxMzgtNzE2NS0yZGY4YzdjNjQ2ZmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTc3NzE4Mjg0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImE3Mzg1MzE1ODItZ21hIn0.ZqMmAbzh-nQbCWUuUuy2I86_CGKqGWyHZvZxVhDe4F0",
  "Accept": "application/vnd.api+json "
}
