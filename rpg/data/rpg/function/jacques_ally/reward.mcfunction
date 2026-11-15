# 雅克战胜利（at 战场中心）：战场里还没有圣殿誓约的人各得一件。
execute as @a[distance=..48,gamemode=!spectator] unless items entity @s container.* *[minecraft:custom_data~{rpg_jq_oath:1b}] unless items entity @s weapon.offhand *[minecraft:custom_data~{rpg_jq_oath:1b}] run function rpg:jacques_ally/reward_one
