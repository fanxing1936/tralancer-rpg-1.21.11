# 死亡会抹掉属性修饰符，复活后重新挂上。附身也随之结束。
scoreboard players set @s rpg_ps_dead 0
scoreboard players set @s rpg_pact_av 0
function rpg:pact/attr
function rpg:pact/seal/apply
execute if score @s rpg_pact matches 1 run function rpg:pact/oath/violate
