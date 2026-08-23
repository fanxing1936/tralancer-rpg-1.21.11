# 一根附赠的箭。pickup:0b —— 凭空造的东西捡不回来，
# 否则这把弓就成了无限箭袋。
summon minecraft:arrow ~ ~ ~ {Tags:["rpg.mam.seen","rpg.mam.new"],pickup:0b,Fire:200s}
execute as @e[type=minecraft:arrow,tag=rpg.mam.new,limit=1] run function rpg:mammon/aim
