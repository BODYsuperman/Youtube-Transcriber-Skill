# 推送到 GitHub 指南

## 📦 文件已准备就绪

所有文件已准备好在：`/tmp/Youtube-Transcriber-Skill/`

### 包含文件

| 文件 | 说明 |
|------|------|
| `README.md` | 完整使用说明（6.5KB） |
| `transcribe.py` | 主脚本（2.2KB） |
| `transcribe_local.py` | 备用脚本（3.3KB） |
| `SKILL.md` | OpenClaw 技能描述 |
| `requirements.txt` | Python 依赖 |
| `.git/` | Git 仓库已初始化 |

---

## 🚀 推送方法

### 方法 1：使用 HTTPS（需要 GitHub Token）

```bash
cd /tmp/Youtube-Transcriber-Skill

# 添加远程仓库
git remote add origin https://github.com/BODYsuperman/Youtube-Transcriber-Skill.git

# 推送到 GitHub
git push -u origin main --force
```

**系统会提示输入：**
- Username: `BODYsuperman`
- Password: [输入你的 GitHub Personal Access Token]

---

### 方法 2：使用 SSH（推荐）

```bash
cd /tmp/Youtube-Transcriber-Skill

# 设置 SSH 远程
git remote set-url origin git@github.com:BODYsuperman/Youtube-Transcriber-Skill.git

# 推送
git push -u origin main --force
```

---

## 🔑 创建 GitHub Personal Access Token

如果使用方法 1（HTTPS），需要创建 Token：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
4. 点击 "Generate token"
5. **复制 Token**（只显示一次！）
6. 在 git push 时用作密码

---

## 📝 验证推送

推送成功后，访问：
https://github.com/BODYsuperman/Youtube-Transcriber-Skill

应该能看到：
- ✅ README.md（带格式说明）
- ✅ transcribe.py（主脚本）
- ✅ 其他文件

---

## 🎯 后续使用

### 更新代码

```bash
# 在本地修改后
cd /tmp/Youtube-Transcriber-Skill
git add .
git commit -m "Update: 描述你的更改"
git push origin main
```

### 其他人使用

```bash
# 克隆仓库
git clone https://github.com/BODYsuperman/Youtube-Transcriber-Skill.git
cd Youtube-Transcriber-Skill

# 安装依赖
pip3 install -r requirements.txt

# 使用
python3 transcribe.py "https://youtube.com/watch?v=VIDEO_ID"
```

---

## 📊 项目信息

- **仓库名：** Youtube-Transcriber-Skill
- **主分支：** main
- **许可证：** MIT
- **Python 版本：** 3.8+

---

## 🙋 常见问题

### Q: 推送失败 "Permission denied"

**A:** 确保你有仓库的写入权限，或使用正确的 Token。

### Q: 找不到 remote "origin"

**A:** 运行 `git remote add origin <URL>` 添加远程仓库。

### Q: 推送被拒绝

**A:** 使用 `--force` 强制推送（如已执行）。

---

**准备好后执行推送命令即可！** 🚀
