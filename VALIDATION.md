# 本机验证记录

日期：2026-10-18，Windows，完整 AutoCAD 2024（引擎 U.61.0.0 / AutoCAD 24.3）。

已完成：

- 使用 skill-installer 下载并安装现成 cad-edit，保留 MIT 许可证；在本包中补充 2024 适配。
- AutoCAD 后台程序 Autodesk 数字签名检查：Valid。
- 官方 quick_validate.py：Skill is valid!（使用 Python -X utf8）。
- demo.py 在 AutoCAD 中生成二维矩形、圆和 BOX 三维实体，保存为原生 DWG。
- 新控制台进程重开 DWG：LWPOLYLINE=1，CIRCLE=1，3DSOLID=1，INSUNITS=4；文件头 AC1032。
- batch.py 先预览清单，再修改独立输出副本；修改后重开检查对象仍为 3 个。
- 通过用户技能目录中实际安装的 core.py 再次读回，CAD-DEMO 图层颜色为 1（红色）；原图为 3（绿色），原图文件和批处理前备份一致。
- 项目技能目录与 Codex 用户技能目录都配置了本机 AutoCAD 路径。

验证限制：

- 第一轮受限环境运行失败：Problem with setting up current profile。正常用户权限重试成功；没有更改 AutoCAD 安全配置来绕过此错误。
- 修复上游控制台 UTF-16 输出及中文 Windows 默认编码导致的日志打印异常。
- 第一次图层示例只创建缺失图层，不修改已存在图层；已修正为 entmod 图层颜色，并重新通过读回验证。
- 已验证引擎生成、保存、重开及图层修改；没有完成 GUI 视觉检查、完整尺寸回读、PDF 出图、动态块或生产图纸验收。
- 这张 DWG 是合成测试图，不是用户附图的户型复原。
- GitHub 目标仓库：https://github.com/3208845485hjp-oss/CAD 。源码、合成示例生成脚本和验证摘要通过 GitHub 连接器提交；不包含本机配置和运行日志。

可查看 examples/verified/verification.json。完整运行日志仅保留在本地，不上传公开仓库。

公开仓库不包含 demo.dwg：自动审批检测到 DWG 内嵌用户/安装元数据并拒绝公开上传。请运行 scripts/demo.py 在本机生成。
