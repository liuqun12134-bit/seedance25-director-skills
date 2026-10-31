# Seedance 2.5 电商口播导演技能

两套独立技能，供支持 SKILL.md 的平台导入。导出版本：2026.10.31.1。

| 技能 | 原插件版本 | 下载 |
| --- | --- | --- |
| 标准口播导演（seedance25-director） | 1.0.1 | [技能 ZIP](https://raw.githubusercontent.com/liuqun12134-bit/seedance25-director-skills/main/dist/seedance25-director.zip) |
| 边讲边使用导演（talk-and-use-director） | 1.0.5 | [技能 ZIP](https://raw.githubusercontent.com/liuqun12134-bit/seedance25-director-skills/main/dist/talk-and-use-director.zip) |

## 安装

把 [导入提示词](IMPORT-PROMPT.md) 发给目标平台。详细步骤见 [INSTALL.md](INSTALL.md)。

每个 ZIP 根目录直接包含 SKILL.md 和 references/，一个包对应一个技能。不要把整个仓库 ZIP 当作单个技能包上传。

## 内容与边界

- 主指令与全部 Markdown 参考资料逐字节保留自上述已安装插件版本。标准版包含 2 份参考资料，使用版包含 5 份。
- 未打包平台专属插件清单、图标、agents/openai.yaml、账号信息、原始图片、视频或音频。
- 标准版侧重自然讲品；使用版侧重真实取用、接触、涂抹/贴膜及状态连续性。请按任务选择，避免同时应用两套冲突的动作规则。
- 技能只设计动作与提示词；不提供 Seedance、Fish Audio 或付费生成权限，也不自动上传用户媒体。
- 本次是原规则的完整导出，不把历史案例当作新任务素材，不声称跨模型输出完全一致。

## 维护

以 skills/ 下的文件作为此仓库母版。更新后同步重建 dist/ 与 manifest.json，再在目标平台更新已安装技能。安装是版本快照，GitHub 更新不会自动传播到 Gemini 或 WorkBuddy。

manifest.json 记录每个文件和 ZIP 的 SHA-256。文件完整性已核验；目标平台的永久安装、音频读取和实际导演效果仍须在对应平台验证。
