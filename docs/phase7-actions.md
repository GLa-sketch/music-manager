# Phase 7 动作表 · 打包与发布

目标：项目完整收尾，能挂简历投实习。

---

## Day 1 · CI + README（助手已写好）

提交后 GitHub Actions 会自动跑 pytest，README 已更新为专业版。

```powershell
git add .
git commit -m "phase7: CI配置与README完善"
git push
```

提交后去 GitHub 仓库页面，点 Actions 标签，能看到 CI 在跑测试。

---

## Day 2 · PyInstaller 打包（可选）

把 GUI 打包成 .exe，双击就能用（不需要 Python 环境）。

```powershell
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "MusicManager" music_manager/gui.py
```

生成的 .exe 在 `dist/MusicManager/` 目录。
（注意：打包 PyQt6 + librosa 体积较大，约 300-500MB，正常现象）

---

## Day 3 · 打 tag 发布 Release

```powershell
git tag v1.0.0
git push origin v1.0.0
```

然后去 GitHub 仓库 → Releases → Create a new release → 选 tag v1.0.0 → 写发布说明 → 发布。

---

## Phase 7 完成标志

- [ ] GitHub Actions CI 能自动跑测试
- [ ] README 专业完整
- [ ] （可选）能打包成 .exe
- [ ] 打了 v1.0.0 tag
- [ ] 项目可以挂简历了
