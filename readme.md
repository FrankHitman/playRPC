# Play RPC
Some reading notes of [深入理解 RPC : 基于 Python 自建分布式高并发 RPC 服务](https://juejin.cn/book/6844733722936377351)


## Preparation for environment
use Python2.7.18 on MacOS 13
```commandline
brew install pyenv
pyenv install 2.7.18
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile

cd path/to/this/folder
pyenv local 2.7.18
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
```

Add existing folder into a GitHub repository, and add a submodule.
```commandline
git init -b main
git remote add origin git@github.com:FrankHitman/playRPC.git
git submodule add git@github.com:FrankHitman/juejin_rpc_py.git
git submodule init
git pull origin main
git branch --set-upstream-to=origin/main main

```

查看依赖与生成依赖文件
```
pip list
pip freeze -> requirements.txt
```

## References
- [深入理解 RPC : 基于 Python 自建分布式高并发 RPC 服务](https://juejin.cn/book/6844733722936377351)


