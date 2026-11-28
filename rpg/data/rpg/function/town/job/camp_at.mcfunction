# 营地的中心：镇中心 + 约 200 格（偏移可能是负数，players add 不收负数）
$scoreboard players set #t rpg_tw $(dx)
scoreboard players operation #px rpg_tw += #t rpg_tw
$scoreboard players set #t rpg_tw $(dz)
scoreboard players operation #pz rpg_tw += #t rpg_tw
