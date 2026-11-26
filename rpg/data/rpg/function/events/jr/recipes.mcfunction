# 配方书（as 玩家）
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[]}
data modify storage rpg:panel ui.title set value ["",{"text":"配方书","color":"#C9A646","bold":true,"italic":false},{"text":" ℜ𝔢𝔠𝔦𝔭𝔢𝔰","color":"#8F7430","bold":false,"italic":false}]
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"配方\n","color":"#9C9A94","bold":true,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"魂火冶炼","color":"#E6DFCF","bold":true,"italic":false},{"text":"　器胚 + 主材（铁锭 ×6 / 钻石 ×4 / 下界合金锭 + 钻石 ×4）+ 残魂 1~3\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"罪器锻造","color":"#E6DFCF","bold":true,"italic":false},{"text":"　武器核心 + 同柱罪印碎片 ×8 + 下界合金锭 + 器胚 + 残魂 ×8，原质 5 阶起，魔化 +15\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"史诗图纸","color":"#E6DFCF","bold":true,"italic":false},{"text":"　图纸 + 特殊材料 ×1 + 钻石 ×6 + 器胚 + 残魂 ×4，原质 4 阶起\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"传说图纸","color":"#E6DFCF","bold":true,"italic":false},{"text":"　图纸 + 特殊材料 ×3 + 下界合金锭 ×2 + 器胚 + 残魂 ×6，原质 6 阶起\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"材料转换","color":"#E6DFCF","bold":true,"italic":false},{"text":"　32 铁锭 + 4 残魂 → 钻石；16 钻石 + 8 残魂 → 下界合金锭；9 金粒 → 金锭；4 金锭 → 镀金箔；10 图纸碎片 → 自选图纸\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"\n材料从哪来\n","color":"#9C9A94","bold":true,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"铁锭","color":"#E6DFCF","bold":true,"italic":false},{"text":"　亡灵、节肢、苦力怕、咒术、末地；精英必掉\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"钻石","color":"#E6DFCF","bold":true,"italic":false},{"text":"　咒术、末地、水域；精英多掉一档\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"下界合金锭","color":"#E6DFCF","bold":true,"italic":false},{"text":"　下界怪物（凋灵骷髅最多）、下界首领\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"残魂 / 器胚","color":"#E6DFCF","bold":true,"italic":false},{"text":"　所有敌对生物、精英、首领\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"罪印碎片","color":"#E6DFCF","bold":true,"italic":false},{"text":"　该柱罪仆、罪仆巡逻\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"图纸","color":"#E6DFCF","bold":true,"italic":false},{"text":"　首领精英、Boss 首杀、坠星与支线；10 片碎片合一张\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"星辰残片","color":"#E6DFCF","bold":true,"italic":false},{"text":"　坠星事件、末地首领\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"风之精魄","color":"#E6DFCF","bold":true,"italic":false},{"text":"　咒术首领（旋风人）\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"深海之泪","color":"#E6DFCF","bold":true,"italic":false},{"text":"　远古守卫者、水域首领\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"熔核","color":"#E6DFCF","bold":true,"italic":false},{"text":"　下界首领\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"山岩之心","color":"#E6DFCF","bold":true,"italic":false},{"text":"　地下（y < 0）的首领\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"圣殿铜","color":"#E6DFCF","bold":true,"italic":false},{"text":"　圣卫\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.body append value {"text":"","extra":[{"text":"墓土","color":"#E6DFCF","bold":true,"italic":false},{"text":"　亡灵首领\n","color":"#9C9A94","bold":false,"italic":false}]}
data modify storage rpg:panel ui.actions append value {"label":{"text":"返回旅程","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_jr_do set 1"}}
data modify storage rpg:panel ui.tab set value 5
function rpg:panel/ui/show with storage rpg:panel ui
