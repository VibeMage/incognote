# Incognote

[English](README.md) · **简体中文**

一个 HTML 文件就是一个纯本地、零上传的 Markdown 笔记本。

用 Chrome 或 Edge 打开 `incognote.html`，选一个放 `.md` 笔记的文件夹，就能浏览、搜索和编辑。笔记始终是你自己文件夹里的普通 Markdown 文件，不会上传到任何地方，页面也从不自己联网加载任何东西。

![阅读笔记](docs/screenshots/zh/reading.png)

## 为什么用它

- **数据不出电脑**：页面带有内容安全策略（CSP `default-src 'none'`），页面发出的任何网络请求都会被浏览器拦截，包括笔记里引用的外部图片。断网也能正常用。（笔记里的网页链接只有在你点击时才会在新标签页打开。）
- **不用安装**：只有一个 HTML 文件，所有代码都内联在里面，没有 CDN、网络字体、统计脚本、服务器或账号。
- **文件还是你的**：Incognote 读写的就是普通 `.md` 文件。同一个文件夹照样可以用别的编辑器、同步工具或 Git。

## 怎么用

只需要下载一个文件。

1. 从[最新版本](https://github.com/VibeMage/incognote/releases/latest)下载 **[incognote.html](https://github.com/VibeMage/incognote/releases/latest/download/incognote.html)**，放在哪里都行，比如放在笔记文件夹旁边。
   也可以在仓库里打开 [incognote.html](incognote.html)，点 **Download raw file** 下载，是同一个文件。
2. 用 **Chrome 或 Edge** 打开它（直接双击文件即可，不需要服务器）。
3. 点 **选择文件夹**，选你的笔记文件夹，在弹窗里允许 **查看和编辑** 文件。
4. 下次打开会回到同一个文件夹。如果 Chrome 再次询问，点 **打开“你的文件夹”**，在提示里选 **每次访问时都允许**，以后打开页面就直接进入笔记。
5. 想换文件夹，点侧边栏底部的文件夹名，里面有最近打开过的文件夹，也可以打开别的文件夹。

> 界面支持中文和英文，默认跟随浏览器语言，也可以点侧边栏顶部的 **EN / 中文** 按钮随时切换，选择会被记住。笔记内容用什么语言都可以。

![选择文件夹](docs/screenshots/zh/welcome.png)

Safari 和 Firefox 不支持写入本地文件夹，在这两个浏览器里会以**只读**方式打开，可以浏览和搜索，不能编辑。

## 功能

| | |
| --- | --- |
| **文件夹** | 左侧是文件夹树，支持多层子文件夹；中间按修改时间列出笔记 |
| **阅读** | Markdown 渲染：标题、表格、可直接勾选的任务列表、代码块、引用、YAML 属性（front matter）、本地图片 |
| **双链** | `[[笔记名]]`、`[[笔记名\|显示文字]]`、`[[笔记名#标题]]`、`![[图片.png]]`；点不存在的链接会新建笔记；每篇笔记底部显示反向链接 |
| **编辑** | ⌘E 切换阅读 / 编辑；输入 `[[` 弹出笔记补全；粘贴截图会存到笔记旁边的 `assets/` 文件夹 |
| **保存** | 停止输入 1.5 秒后自动保存，⌘S 立即保存；关闭页面前如有未保存内容会提醒 |
| **冲突** | 保存前检查文件是否在别处（另一个编辑器、同步工具）被改过，改过会先问你 |
| **管理** | 新建、重命名（会同步更新其他笔记里指向它的双链）、删除（先确认，永久删除） |
| **搜索** | ⌘K 搜索所有笔记，多个关键词用空格分隔；结果按“文件名”和“正文”分组并高亮 |
| **外观** | 跟随系统浅色 / 深色 |
| **语言** | 中文和英文界面；默认跟随浏览器，可随时切换并记住选择 |

Windows 和 Linux 上用 Ctrl 代替 ⌘，界面会自动显示对应的按键。

![全局搜索](docs/screenshots/zh/search.png)

![编辑和双链补全](docs/screenshots/zh/editing.png)

![深色模式、属性和反向链接](docs/screenshots/zh/dark.png)

截图用的是一个虚构的示例笔记文件夹。

## 实现原理

Incognote 是一个没有后端的普通网页，所有事情都在浏览器标签页里完成。

**文件夹访问**：使用浏览器的 [File System Access API](https://developer.mozilla.org/docs/Web/API/File_System_API)。`showDirectoryPicker({ mode: 'readwrite' })` 让页面拿到你所选文件夹（且仅限这个文件夹）的句柄。最近打开的几个文件夹的句柄保存在页面的 IndexedDB 里。页面加载时对上次的文件夹调用 `queryPermission()`：如果 Chrome 仍允许访问（比如选过“每次访问时都允许”），就直接进入；否则点一下按钮调用 `requestPermission()`，这一步浏览器要求必须由用户点击触发。不支持这个 API 的浏览器退回到 `<input webkitdirectory>`，只能只读。

**建立索引**：打开文件夹时遍历所有 `.md` 文件读入内存，提取标题（第一个 `# 标题`、属性里的 `title`，或文件名）、预览摘要和其中的双链。`.git`、`.obsidian` 等隐藏文件夹和 `node_modules` 会被跳过。标签页重新获得焦点时会重新扫描，只重读修改时间变了的文件。

**渲染**：Markdown 由 markdown-it 解析，并加了几条自定义规则来支持双链、图片嵌入和可勾选的任务列表。生成的 HTML 先经过 DOMPurify 清洗再显示，所以笔记内容无法执行脚本或注入样式。本地图片从文件夹读出后通过 `blob:` 地址显示。

**搜索**：在内存里对所有笔记的全文做匹配，几千篇以内都是即时出结果。所有关键词都要命中；文件名命中的排在前面。

**保存**：每篇打开的笔记都记着它开始编辑时的原文。写入前会重新读取磁盘上的文件，如果期间被别处改过，会先问你是否覆盖。重命名时会改写其他笔记里的 `[[链接]]`，``` 代码块和行内代码里的内容不动。

**零联网**：文件开头的内容安全策略是 `default-src 'none'`，只放行页面自带的内联脚本和样式、`blob:` 和 `data:` 图片，以及 `blob:` 媒体，并设置了 `base-uri 'none'` 和 `form-action 'none'`。即使笔记里写了 `<img src="https://…">`，浏览器也会拒绝加载。你可以在开发者工具的 Network 面板里自己验证。

### 用到的库

两个库都已打包进 HTML 文件，运行时不会加载任何外部资源。

| 库 | 版本 | 用途 | 许可证 |
| --- | --- | --- | --- |
| [markdown-it](https://github.com/markdown-it/markdown-it) | 14.1.0 | 把 Markdown 解析成 HTML | MIT |
| [DOMPurify](https://github.com/cure53/DOMPurify) | 3.2.6 | 清洗渲染出的 HTML，防止脚本注入 | Apache-2.0 或 MPL-2.0 |

其余部分（文件读写、双链、搜索、编辑器、界面）都是不依赖框架的原生 JavaScript 和 CSS。图标是按 SF Symbols 风格手绘的 SVG。两个库的许可证原文在 `src/vendor/`。

## 开发

```
src/app.html          应用源码（HTML、CSS、JS）
src/icons.json        SVG 图标
src/vendor/           markdown-it 和 DOMPurify 及其许可证
build.py              把所有内容内联成 incognote.html
incognote.html        构建好的单文件
```

改了 `src/` 里的内容后重新构建：

```sh
python3 build.py
```
