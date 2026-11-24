execute at @e[type=minecraft:wolf,name="大团长",distance=..16,limit=1] run particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.6 0.3 0.02 20
tellraw @s ["",{"text":"（残影朝那只狗低头行了一礼。）","color":"#797979","bold":false,"italic":false}]
function rpg:quest/title/get_grandmaster
