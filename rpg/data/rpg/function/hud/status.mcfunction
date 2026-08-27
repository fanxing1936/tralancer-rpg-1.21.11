# 屏幕下方的持续状态行：魔化（或圣痕）、契约对象、七柱冷却、上位契约冷却四槽。
#
# 命令拼不了字符串，所以四槽各自选好文本存进 storage，
# 最后由一条宏拼成一行。storage 是全局的，但整个计算与渲染
# 发生在同一个玩家的同步执行里，中间插不进别人。
scoreboard players set @s rpg_hud_on 0
data modify storage rpg:hud a set value '{"text":""}'
data modify storage rpg:hud b set value '{"text":""}'
data modify storage rpg:hud c set value '{"text":""}'
data modify storage rpg:hud d set value '{"text":""}'
execute unless score @s rpg_lt_divine matches 2 if entity @s[scores={rpg_holy=1..}] run function rpg:hud/holy
execute unless score @s rpg_lt_divine matches 2 if entity @s[scores={rpg_taint=1..}] run function rpg:hud/taint
execute if score @s rpg_lt_divine matches 2 run function rpg:hud/authority
execute if entity @s[scores={rpg_pact=1..7}] run function rpg:hud/pact
execute if entity @s[scores={rpg_pact_cd=1..}] run function rpg:hud/pbar
execute if score @s rpg_lt_div_cd matches 1.. run function rpg:hud/divine_bar
execute if entity @s[scores={rpg_hud_dmt=1..},tag=rpg.seal.carrier] run function rpg:hud/demon/render with storage rpg:hud
execute if entity @s[scores={rpg_hud_on=1,rpg_hud_dmt=1..},tag=!rpg.seal.carrier] run function rpg:hud/demon/render with storage rpg:hud
execute if entity @s[scores={rpg_hud_dmt=0},tag=rpg.seal.carrier] run function rpg:hud/seal/render with storage rpg:hud
execute if entity @s[scores={rpg_hud_on=1,rpg_hud_dmt=0},tag=!rpg.seal.carrier] run function rpg:hud/render with storage rpg:hud
execute if entity @s[scores={rpg_hud_on=0,rpg_hud_dmt=1..},tag=!rpg.seal.carrier] run function rpg:hud/demon/solo
