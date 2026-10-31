# 导入说明

## 下载与核验

先读取 [manifest.json](https://raw.githubusercontent.com/liuqun12134-bit/seedance25-director-skills/main/manifest.json)，下载其中两份 zip_url。SHA-256 可核对下载完整性，不是独立签名或身份认证。完整保存 references/，不要只提取或概括 SKILL.md。

## WorkBuddy

优先通过当前平台明确支持的本地技能安装能力完成安装；不要猜测目录或虚构安装接口。若对话中没有这样的能力，下载 ZIP 后由用户在「专家·技能·连接器 → 技能 → 添加技能 → 上传技能」分别上传两份包。

官方说明只明确支持通过上传入口导入自定义技能包，不能保证任意账号收到 GitHub 链接后即可自动安装。安装完成后在已安装列表核验两个技能名称。已经存在同名技能且有本地改动时，先保留备份，不静默覆盖。

官方文档：https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market

## Gemini 网页版

如果当前账号提供对话创建技能能力，可以尝试完整读取各技能和参考文件后创建两个独立技能；仅在平台实际保存了完整资料且可再次调用时才报告安装成功。GitHub URL 本身不是安装接口，读取网页也不等于永久保存技能。

可靠的上传路径：「Customize → Skills → Create → Upload」，分别上传两个 ZIP。更新已有技能使用「Replace skill」。如果账号未提供 Skills，说明账号入口限制；可另行采用 Gems 指令和知识文件方案，但不能声称已安装 Skill。

官方文档：https://support.google.com/gemini/answer/17094296

## 验收

1. 两个独立技能分别显示为 seedance25-director 与 talk-and-use-director。
2. 标准版有 SKILL.md 与 2 份 references 文件；使用版有 SKILL.md 与 5 份 references 文件；文件清单见 manifest.json。
3. 新对话能重新选用技能。若未能验证新对话持久调用，明确标注未验证。
4. 真实任务再上传首帧、人物参考、产品参考和完整音频。音频不能读取时应如实说明；无可靠时间戳时不得声称精确逐句对齐。

安装时无需生成视频、付费或上传任何真实素材。
