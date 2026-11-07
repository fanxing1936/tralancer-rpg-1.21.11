# 从圣卫战开始完整战斗。
execute if score #stage rpg_pf matches 1.. run return run tellraw @s ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"已有一场教皇战；先用 /function rpg:pope_fight/clear 清场。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:pope_fight/begin
function rpg:pope_fight/stage1_enter
