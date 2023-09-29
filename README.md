# eLLM

## Getting Started


```shell
pip install -r requirements.txt
python login.py
```

Second terminal:
```shell
curl --location 'http://127.0.0.1:8000/signup' \
--form 'username="arushisharma"' \
--form 'email="arushi@test.com"' \
--form 'password="test123"'
```

To check data stored in MongoDB compass:
Connection String: mongodb://127.0.0.1:27017/llm?authSource=admin
