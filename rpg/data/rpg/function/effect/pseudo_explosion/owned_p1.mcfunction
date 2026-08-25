
# 调用时 @s 是真实施法者；同步临时标签不会跨玩家、跨刻泄漏。
tag @e[tag=rpg.pseudo_boom.source] remove rpg.pseudo_boom.source
tag @s add rpg.pseudo_boom.source
function rpg:effect/pseudo_explosion/sourced_p1
tag @s remove rpg.pseudo_boom.source
