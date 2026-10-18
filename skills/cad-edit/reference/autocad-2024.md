# AutoCAD 2024 本机适配

此包复用 xy425yi/claude-cad-skill 的 MIT 源码。优先采用本页的版本限制；上游对 2027 DLL、完整功能的描述不适用于本包。

- 使用合法安装且已激活的完整 AutoCAD 2024；不要启用 --dyn。本包移除了上游预编译 DLL。三维实体通过原生 BOX、EXTRUDE 等 AutoLISP command 命令创建。
- core.py 只使用 Python 标准库；PDF/DXF 辅助工具需仓库 requirements.txt 中依赖。使用安装教程所列虚拟环境 Python 的完整路径。
- 本机 cadcore.json 可含 python 和 project 字段，分别给出解释器与适配包路径；先读配置，再定位仓库示例脚本。不要假设系统 PATH 中有 python。
- 当前机器路径写在 cadcore.json；迁移电脑时重新配置，不提交本机配置。
- 新图：明确毫米单位、WCS、对象捕捉关闭。仓库 scripts/demo.py 展示二维矩形、圆和三维实体生成与 DWG 保存/重开。
- 批量修改优先使用仓库 scripts/batch.py，先列清单，再 --apply。它修改独立目录内的副本并保留备份。外部参照应保持目录关系；该简单脚本不会打包外部参照，含 xref 的项目需先单独准备完整项目副本。
- --readonly 只是读取模式约定，不是任意 LISP 的安全沙箱；代码中的 SAVEAS/文件函数仍可能写文件。运行前审查代码。不要以 --readonly 作为执行未知脚本的保证。
- 上游驱动在控制台进程中使用 SECURELOAD=0 加载 LISP；不要手动更改用户桌面 AutoCAD 的安全设置。上游会整理图纸目录的 ErrorReports/plot.log，因此只在独立工作副本上运行。
- 附图仅是参考，不能从像素推断未标注尺寸、墙厚、门洞或结构。用户明确要求复原时先建立尺寸表，记录歧义；不要把本包示例称为该户型的精确复原或施工图。
- 交付报告区分：语法/结构检查、引擎保存成功、重开读回、几何尺寸检查、视觉检查；只声称实际完成的层级。
