data modify storage rpg:panel ui.title set value {"text":"操作速查","color":"#9C9A94","bold":true,"italic":false,"extra":[{"text":" ℌ𝔞𝔫𝔡𝔟𝔬𝔬𝔨","color":"#8F7430","bold":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"面板：切到玩家面板并停留片刻就会打开；切走再切回可重开。","color":"#9C9A94","italic":false},{"text":"\n"}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"真名：携带圣器，见证同一恶魔三种不同招式。","color":"#9C9A94","italic":false},{"text":"\n"}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"仪式：点燃图腾 → 投入媒介 → 宣读真名 → 选择裁决。","color":"#9C9A94","italic":false},{"text":"\n"}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"告解铃可打断反仪式；圣钉、粉笔与净罪香投入法阵生效。","color":"#9C9A94","italic":false},{"text":"\n"}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"所有面板按钮仅作用于点击者，不要求管理员权限。","color":"#797979","italic":false},{"text":"\n"}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"契约：长按放力量，潜行长按放魂誓技能，潜行抬头长按化身，潜行低头长按打开契约。","color":"#9C9A94","bold":false,"italic":false},{"text":"\n"}]}
data modify storage rpg:panel ui.actions append value {"label":{"text":"返回面板","color":"#C9A646","italic":false,"bold":true},"action":{"type":"minecraft:run_command","command":"/trigger rpg_panel set 8"}}
