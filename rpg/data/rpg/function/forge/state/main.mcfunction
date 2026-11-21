tag @s add rpg.fg.m
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{kind:"melee"}}] run tag @s add rpg.fg.k.melee
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{kind:"ranged"}}] run tag @s add rpg.fg.k.ranged
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{lv:10}}] run tag @s add rpg.fg.lv10
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"none"}}] run tag @s add rpg.fg.st
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{src:"faith"}}] run tag @s add rpg.fg.src.faith
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{src:"hope"}}] run tag @s add rpg.fg.src.hope
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{src:"resolve"}}] run tag @s add rpg.fg.src.resolve
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{src:"malice"}}] run tag @s add rpg.fg.src.malice
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{src:"hatred"}}] run tag @s add rpg.fg.src.hatred
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{src:"pride"}}] run tag @s add rpg.fg.src.pride
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["ember"]}}] run tag @s add rpg.fg.r.ember
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["echo"]}}] run tag @s add rpg.fg.r.echo
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["execute"]}}] run tag @s add rpg.fg.r.execute
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["backstab"]}}] run tag @s add rpg.fg.r.backstab
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["bloodpact"]}}] run tag @s add rpg.fg.r.bloodpact
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["poise"]}}] run tag @s add rpg.fg.r.poise
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["hunt"]}}] run tag @s add rpg.fg.r.hunt
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["split"]}}] run tag @s add rpg.fg.r.split
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{runes:["meteor"]}}] run tag @s add rpg.fg.r.meteor
execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"rift"}}] run tag @s add rpg.fg.st.rift
execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"frost"}}] run tag @s add rpg.fg.st.frost
execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"shadow"}}] run tag @s add rpg.fg.st.shadow
execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"blood"}}] run tag @s add rpg.fg.st.blood
execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"gale"}}] run tag @s add rpg.fg.st.gale
execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"volley"}}] run tag @s add rpg.fg.st.volley
execute if entity @s[tag=rpg.fg.st] if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_eq:{stone:"banner"}}] run tag @s add rpg.fg.st.banner
