advancement revoke @s only rpg:pact/seal
execute if entity @s[scores={rpg_pact_t=1..}] run return 0
scoreboard players set @s rpg_pact_t 8
execute unless entity @s[tag=rpg.pact] run return run function rpg:pact/say/seal_nopact
scoreboard players set #seal rpg_pact 0
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:1}] run scoreboard players set #seal rpg_pact 1
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:2}] run scoreboard players set #seal rpg_pact 2
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:3}] run scoreboard players set #seal rpg_pact 3
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:4}] run scoreboard players set #seal rpg_pact 4
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:5}] run scoreboard players set #seal rpg_pact 5
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:6}] run scoreboard players set #seal rpg_pact 6
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:7}] run scoreboard players set #seal rpg_pact 7
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:8}] run scoreboard players set #seal rpg_pact 8
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:9}] run scoreboard players set #seal rpg_pact 9
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:10}] run scoreboard players set #seal rpg_pact 10
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:11}] run scoreboard players set #seal rpg_pact 11
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:12}] run scoreboard players set #seal rpg_pact 12
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:13}] run scoreboard players set #seal rpg_pact 13
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:14}] run scoreboard players set #seal rpg_pact 14
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:15}] run scoreboard players set #seal rpg_pact 15
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:16}] run scoreboard players set #seal rpg_pact 16
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:17}] run scoreboard players set #seal rpg_pact 17
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:18}] run scoreboard players set #seal rpg_pact 18
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:19}] run scoreboard players set #seal rpg_pact 19
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:20}] run scoreboard players set #seal rpg_pact 20
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:21}] run scoreboard players set #seal rpg_pact 21
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:22}] run scoreboard players set #seal rpg_pact 22
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:23}] run scoreboard players set #seal rpg_pact 23
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:24}] run scoreboard players set #seal rpg_pact 24
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:25}] run scoreboard players set #seal rpg_pact 25
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:26}] run scoreboard players set #seal rpg_pact 26
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:27}] run scoreboard players set #seal rpg_pact 27
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:28}] run scoreboard players set #seal rpg_pact 28
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:29}] run scoreboard players set #seal rpg_pact 29
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:30}] run scoreboard players set #seal rpg_pact 30
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:31}] run scoreboard players set #seal rpg_pact 31
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:32}] run scoreboard players set #seal rpg_pact 32
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:33}] run scoreboard players set #seal rpg_pact 33
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:34}] run scoreboard players set #seal rpg_pact 34
execute if items entity @s weapon.* *[minecraft:custom_data~{rpg_seal:35}] run scoreboard players set #seal rpg_pact 35
execute if score #seal rpg_pact matches 0 run return 0
execute if score @s rpg_pact_lv matches 2.. if score @s rpg_pact_s1 matches 0 run return run function rpg:pact/seal/put1
execute if score @s rpg_pact_lv matches 3.. if score @s rpg_pact_s2 matches 0 run return run function rpg:pact/seal/put2
function rpg:pact/say/seal_full
