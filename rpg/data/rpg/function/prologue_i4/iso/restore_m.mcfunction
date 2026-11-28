$execute unless data storage rpg:pr_i4 r.p$(id) run return run tellraw @s {"text":"[序章] 找不到你的回程记录","color":"red"}
effect clear @s
$function rpg:prologue_i4/iso/back with storage rpg:pr_i4 r.p$(id)
$data remove storage rpg:pr_i4 r.p$(id)
