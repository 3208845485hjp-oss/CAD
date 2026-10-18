# AutoCAD 2024 + Codex 新手使用教程

这是在现成开源 cad-edit skill 上制作的 AutoCAD 2024 适配包，不是从零编写的 CAD 引擎。保留上游 MIT 许可证与源文件。技能让 Codex 调用本机 AutoCAD 的后台程序，读取、修改和保存真正的 DWG。

## 能做什么

- 二维：线、多段线、圆、图层、文字、尺寸及已有图纸修改。
- 三维：完整 AutoCAD 中通过原生 AutoLISP 命令创建实体；本包演示长方体。
- 批处理：先列出计划，再修改独立目录里的副本。
- DWG 输出：用 AutoCAD SAVEAS/QSAVE 保存；DXF 只作示例的中间输入，不冒充 DWG。

本包禁用上游面向 AutoCAD 2027 的 dynblock.dll。动态块参数和 .NET 表格 API 不在 2024 验证范围。PDF 功能来自上游，需单独检查打印机与 CTB，未经过本项目验证。

## 安装

1. 安装并打开过合法授权的完整 AutoCAD 2024，确认普通图纸能打开。后台引擎仍然需要 AutoCAD 许可。
2. 安装 Python 3.12（官方 python.org），安装时勾选 Add Python to PATH。
3. 下载本仓库 ZIP 并解压。文件夹里应能看见 skills、scripts 和 requirements.txt。
4. 在该文件夹打开 PowerShell，执行下面命令。`-AutoCAD` 改成你电脑的安装目录。

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1 -AutoCAD 'D:\CAD2024\AutoCAD 2024' -Python python
```

脚本检查 Autodesk 数字签名，为本项目创建 `.venv`，安装 PyPI 依赖，再复制技能到 Codex 用户技能目录。它不会更改系统执行策略；如果已有 cad-edit，会停止，防止覆盖。

安装后，下一个 Codex 回合即可发现技能；如果列表尚未刷新，新开聊天。使用 `$cad-edit` 明确指定。Codex 官方说明：https://developers.openai.com/codex/skills

当前交付时使用的独立 Python 位于本工作区 `work/venv/Scripts/python.exe`。它不是系统 Python；换电脑请按上面的步骤重新安装。

## 验证二维、三维和 DWG

在仓库根目录运行；输出目录必须是新的，避免覆盖：

```powershell
.\.venv\Scripts\python.exe .\scripts\demo.py --out .\demo-run-01
```

预期生成 `demo.dwg`、创建日志、重开日志和 verification.json。示例包括毫米单位的 6000×4000 矩形、半径 500 的圆、2000×1000×1500 长方体。脚本用 AutoCAD 保存 DWG，再在新进程中重开检查三种对象各 1 个、单位为毫米和 DWG 文件头。尺寸预期也记录在报告中；脚本对象计数不等同于完整尺寸或视觉审查。

双击 DWG 用 AutoCAD 打开，`ZOOM` → `E` 查看全部；切换等轴测视图查看长方体。示例是合成测试图，不是附图户型复原。

## 验证批量修改

把测试 DWG 放进 `input-drawings`；`modified-drawings` 必须是独立空目录。先预览：

```powershell
.\.venv\Scripts\python.exe .\scripts\batch.py --input .\input-drawings --output .\modified-drawings --lisp .\examples\change-layer.lsp
```

检查文件清单后，在同一命令末尾加 `--apply`。此示例把 CAD-DEMO 图层改成红色，只修改输出副本，并产生备份。外部参照不随这个简单脚本复制，含外部参照的实际项目需先准备完整项目副本。

## 在 Codex 中怎么说

```text
请使用 $cad-edit，先读取这个 DWG 的单位、图层和对象，暂时不要修改。使用安装教程里的虚拟环境 Python。
```

```text
请使用 $cad-edit，在新文件中创建毫米单位的二维房间草图，6000×4000，墙厚200。先列出尺寸和假设，生成 DWG 后重开核对。
```

```text
请使用 $cad-edit，对这个文件夹里的 DWG 批量改图层颜色。先列清单，只在独立副本目录中修改，保留原图和备份，并读回核对实际颜色。
```

附图能帮助说明布局，但不能可靠给出全部墙厚、门洞和未标注尺寸。需要按图片画图时，先核对尺寸表与不明确之处。

## 上传到 GitHub

推荐私有仓库，名称 autocad-2024-codex-skill。本项目不应上传密码、令牌、个人户型参考图、cadcore.json 或实际业务图纸。

如果尚未连接：在 Codex 的 GitHub 连接设置中授权所需仓库；浏览器登录与连接器授权是两件事。不要把密码或令牌发给助手。

网页上传备用方式：打开仓库 → Add file → Upload files，将本项目源码目录中的文件和文件夹拖进去，保留目录结构 → Commit changes。不要上传 `.venv`。若工具尚不能创建仓库，访问 https://github.com/new，填写名称、选 Private 后 Create repository。

## 来源与改动

- 上游：https://github.com/xy425yi/claude-cad-skill ，MIT，见 LICENSE。
- 增加本中文教程、2024 版本限制、setup.ps1、demo.py、batch.py 和合成示例。
- 删除上游预编译 DLL，禁用 --dyn。上游其余脚本保留，不能据此宣称全功能在本机已通过验证。
- 查看 VALIDATION.md 了解本机实际验证结果。

## 仓库中的示例

公开仓库提供示例生成脚本及验证摘要，不提交 DWG 二进制文件，以避免公开 AutoCAD 写入的用户/安装元数据。按上面的 demo.py 命令即可在本机生成 DWG。
