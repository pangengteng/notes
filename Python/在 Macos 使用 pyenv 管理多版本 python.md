# pyenv

## 安装 pyenv
```bash
brew update
brew install openssl readline sqlite3 xz zlib pyenv
```

## 安装制定版本的python
```bash
pyenv install 3.13.5
```

## 查看已安装的python版本
```bash
pyenv versions
```

## 设置python版本

### 当前会话
```bash
pyenv shell 3.13.5

# 如果出现错误提示：pyenv: shell integration not enabled. Run `pyenv init' for instructions.
# 则先执行 pyenv init，根据提示把脚本添加到对应的文件即可

# 验证版本生效
python --version
```

### 当前目录
```bash
pyenv local 3.13.5

## 修改
pyenv local 3.9.18

## 清除
pyenv local --unset
```

### 全局
```bash
pyenv global 3.13.5

## 还原为系统默认值
pyenv global system
```

> 优先级为：shell > local > global > system