execute unless score @s rpg_ch1_next matches 1.. run return run tellraw @s ["",{"text":"[权限不足] 完成第一章后开放。","color":"#8B2500","bold":false,"italic":false}]
tellraw @s ["",{"text":"[高阶追踪] ","color":"#C9B5FF","bold":true,"italic":false},{"text":"第二档案：路西法 · 王冠失窃案","color":"gray","bold":false,"italic":false}]
tellraw @s ["",{"text":"北部圣库的加冕圣物失踪；现场只留下一根向下坠落的羽毛。","color":"#706B5E","bold":false,"italic":false}]
function rpg:panel/inquest
