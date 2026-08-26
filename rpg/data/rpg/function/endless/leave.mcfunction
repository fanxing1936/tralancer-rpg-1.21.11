scoreboard players set @s rpg_end_leave 0
function rpg:endless/member/clear_boons
tag @s remove rpg.end.member
tag @s remove rpg.end.member.current
tellraw @s ["",{"text":"[已离开] ","color":"#FF665E","bold":true,"italic":false},{"text":"本轮圣恩与断罪层数已冻结；历史最深层保留。","color":"#AAB4C3","bold":false,"italic":false}]
