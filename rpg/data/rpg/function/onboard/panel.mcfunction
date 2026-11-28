# 「序章」按钮：只给还没打完序章的人（用户 2026-11-28「序章结束就从菜单移除掉」）
execute unless entity @s[tag=rpg.pr] unless score @s rpg_pr_done matches 1.. run data modify storage rpg:panel ui.actions append value {"label":{"text":"序章","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pro_go set 1"}}
execute unless score @s rpg_ident matches 1.. run return 0
execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
data modify storage rpg:onboard tmp.i set value {n:"",c:"#FFFFFF"}
execute if score @s rpg_ident matches 1 run data modify storage rpg:onboard tmp.i set value {n:"无知者",c:"#B8B2A4"}
execute if score @s rpg_ident matches 2 run data modify storage rpg:onboard tmp.i set value {n:"边缘者",c:"#9B6BD6"}
execute if score @s rpg_ident matches 3 run data modify storage rpg:onboard tmp.i set value {n:"神职者",c:"#E8D9B0"}
execute if score @s rpg_ident matches 4 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆",c:"#C04848"}
execute if score @s rpg_ident matches 5 run data modify storage rpg:onboard tmp.i set value {n:"圣子",c:"#FFD85A"}
execute if score @s rpg_ident matches 6 run data modify storage rpg:onboard tmp.i set value {n:"圣灵",c:"#F4F0FF"}
execute if score @s rpg_ident matches 7 run data modify storage rpg:onboard tmp.i set value {n:"弥赛亚",c:"#FFF2A8"}
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 1 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆 · 路西法之傲慢",c:"#5FD68C"}
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 2 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆 · 利维坦之嫉妒",c:"#4F9EF0"}
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 3 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆 · 亚巴顿之怠惰",c:"#A7AFC9"}
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 4 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆 · 别西卜之暴食",c:"#B5D957"}
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 5 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆 · 萨麦尔之暴怒",c:"#FF5C52"}
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 6 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆 · 贝利尔之色欲",c:"#D97AD9"}
execute if score @s rpg_ident matches 4 if score @s rpg_ident_sin matches 7 run data modify storage rpg:onboard tmp.i set value {n:"七大罪之仆 · 玛门之贪婪",c:"#E6A23C"}
data modify storage rpg:onboard tmp.i.id set from storage rpg:onboard tmp.id
function rpg:onboard/panel_m with storage rpg:onboard tmp.i
