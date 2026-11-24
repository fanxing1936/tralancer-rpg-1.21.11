# 契约之书上按 F：化身；Shift+F：打开契约（as/at 玩家，书已换回原手）。
execute unless entity @s[tag=rpg.pact] run return run tellraw @s {"text":"这本书还没立约：长按右键翻开条款","color":"gray","italic":false}
tag @s remove rpg.pact.off
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact_tag:1b}] run tag @s add rpg.pact.off
execute unless entity @s[tag=rpg.pact.off] unless items entity @s weapon.mainhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/reissue
execute if entity @s[tag=rpg.pact.off] unless items entity @s weapon.offhand *[minecraft:custom_data~{pact_signed:1b}] run return run function rpg:pact/reissue
execute unless score @s rpg_pact_lv matches 1.. run function rpg:pact/oath/migrate
function rpg:pact/book/stale
execute if predicate rpg:sneaking run return run function rpg:pact/ui/open
function rpg:pact/depth/avatar
