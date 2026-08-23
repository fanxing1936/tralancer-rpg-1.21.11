# 屏幕下方的持续状态行：魔化（或圣痕）在左，契约冷却在右。
#
# 命令拼不了字符串，所以两半各自按分数选好自己那段存进 storage，
# 最后由一条宏拼成一行。storage 是全局的，但整个计算与渲染
# 发生在同一个玩家的同步执行里，中间插不进别人。
scoreboard players set @s rpg_hud_on 0
data modify storage rpg:hud a set value '{"text":""}'
data modify storage rpg:hud b set value '{"text":""}'
execute if entity @s[scores={rpg_holy=1..}] run function rpg:hud/holy
execute if entity @s[scores={rpg_taint=1..}] run function rpg:hud/taint
execute if entity @s[scores={rpg_pact_cd=1..}] run function rpg:hud/pbar
execute if entity @s[scores={rpg_hud_on=1}] run function rpg:hud/render with storage rpg:hud
