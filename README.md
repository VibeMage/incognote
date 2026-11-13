# Incognote

纯本地、零上传的 Markdown 笔记本。

一个网页文件就是一个笔记本：用 Chrome 或 Edge 打开 `incognote.html`，选一个放 Markdown 笔记的文件夹，就能浏览、搜索、编辑。

- **纯本地、零上传**：笔记始终是你文件夹里的 `.md` 文件。页面带有内容安全策略（CSP `default-src 'none'`），浏览器会拦截一切网络请求，包括笔记里引用的外部图片。断网也能用。
- **不用安装**：只有一个 HTML 文件，所有代码都在里面，没有 CDN、字体服务或统计脚本。

## 怎么用

1. 下载 [`incognote.html`](incognote.html)，放在哪里都行。
2. 用 Chrome 或 Edge 打开它，点“选择文件夹”，选你的笔记文件夹，在弹窗里允许“查看和编辑”。
3. 下次打开时点“继续使用上次的文件夹”，Chrome 会请你再点一次“允许”。

Safari 和 Firefox 不支持写入本地文件夹，只能以只读方式浏览和搜索。

## 功能

| 功能 | 说明 |
| --- | --- |
| 文件夹 | 左侧是文件夹树，支持多层子文件夹；中间是按修改时间排列的笔记 |
| 阅读 | Markdown 渲染：标题、表格、任务列表（可直接勾选）、代码块、引用、本地图片 |
| 双链 | `[[笔记名]]`、`[[笔记名\|显示文字]]`、`[[笔记名#标题]]`、`![[图片.png]]`；点不存在的链接会新建笔记；笔记底部显示反向链接 |
| 编辑 | ⌘E 切换阅读 / 编辑；输入 `[[` 弹出笔记补全；粘贴截图会存到笔记旁边的 `assets/` 文件夹 |
| 保存 | 停止输入 1.5 秒自动保存，⌘S 立即保存；关闭页面前有未保存内容会提醒 |
| 冲突 | 保存前检查文件是否在别处（比如另一个编辑器）被改过，被改过会先问你 |
| 管理 | 新建、重命名（会同步更新其他笔记里指向它的双链）、删除（永久删除，会先确认） |
| 搜索 | ⌘K 搜索所有笔记，多个关键词用空格分隔；结果分“文件名”和“正文”两组并高亮 |
| 外观 | 跟随系统浅色 / 深色 |

## 开发

源码在 `src/app.html`，第三方库在 `src/vendor/`。修改后运行：

```sh
python3 build.py
```

会重新生成单文件 `incognote.html`。

## 第三方组件

- [markdown-it](https://github.com/markdown-it/markdown-it) 14.1.0，MIT 许可，见 `src/vendor/LICENSE-markdown-it`
- [DOMPurify](https://github.com/cure53/DOMPurify) 3.2.6，Apache-2.0 或 MPL-2.0 许可，见 `src/vendor/LICENSE-dompurify`
- 图标按 Cupertino 设计系统的 SF Symbols 风格替代图标绘制
