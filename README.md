# Seedance 2.5 电商口播导演技能

两套独立技能，供支持 SKILL.md 的平台导入。导出版本：2026.11.01.1。

| 技能 | 原插件版本 | 下载 |
| --- | --- | --- |
| 标准口播导演（seedance25-director） | 1.0.1 | [技能 ZIP](https://raw.githubusercontent.com/liuqun12134-bit/seedance25-director-skills/main/dist/seedance25-director.zip) |
| 边讲边使用导演（talk-and-use-director） | 1.0.5 | [技能 ZIP](https://raw.githubusercontent.com/liuqun12134-bit/seedance25-director-skills/main/dist/talk-and-use-director.zip) |

## 安装

把 [导入提示词](IMPORT-PROMPT.md) 发给目标平台。详细步骤见 [INSTALL.md](INSTALL.md)。

每个 ZIP 根目录直接包含 SKILL.md、references/、scripts/、templates/、agents/ 和 learning-config.json，一个包对应一个技能。不要把整个仓库 ZIP 当作单个技能包上传。

## 内容与边界

- 保留原有动作与案例参考资料，两个独立 Skill 均更新至 1.1.0，增加可开关自优化、持久个人经验与策略库。标准版同步规范正式提示词的素材编号和外部画幅设置边界。
- 包含可选 agents/openai.yaml、标准库学习脚本和模板；不包含平台插件清单、账号、原始媒体或私人学习数据。
- 标准版侧重自然讲品；使用版侧重真实取用、接触、涂抹/贴膜及状态连续性。请按任务选择，避免同时应用两套冲突的动作规则。
- 技能只设计动作与提示词；不提供 Seedance、Fish Audio 或付费生成权限，也不自动上传用户媒体。
- 本版是保留原动作规则的自优化升级，不把历史案例当作新任务素材，不声称跨模型输出完全一致。

## 维护

以 skills/ 下的文件作为此仓库母版。更新后同步重建 dist/ 与 manifest.json，再在目标平台更新已安装技能。安装是版本快照，GitHub 更新不会自动传播到 Gemini 或 WorkBuddy。

manifest.json 记录每个文件和 ZIP 的 SHA-256。文件完整性已核验；目标平台的永久安装、音频读取和实际导演效果仍须在对应平台验证。

## 自优化

默认关闭。可说“开启两个导演的自优化”，或分别开启/关闭；任务结束时有新经验才记。模型自评不等于用户确认，自动策略提升需至少两个独立任务。开关和个人库外置于 `.local/share/skill-learning/`（可配置 SKILL_LEARNING_HOME），升级保留、迁移另行备份，不随仓库同步。完整说明在各 Skill 的 references/self-optimization.md。没有实际成片时不宣称口型或动作连续性已经验证。
