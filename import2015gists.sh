#!/usr/bin/env bash

add_remote() {
    day=$1
    gist=$2
    git remote add "2015day$day" "git@github.com:$gist.git"
}

make_day_branch_from() {
    day=$1
    base_remote="2015day$2"
    git checkout --orphan "2015day$day"
    git reset --hard
    git fetch $base_remote
    git cherry-pick "$base_remote/master" --allow-empty-message
    git push
}

add_remote 6 31bb28b88fe24c9e703e
make_day_branch_from 6 6

add_remote 7.1 1dda6233205d2a668038
add_remote 7.2 e52029359d3e1cc163af
make_day_branch_from 7 7.1

add_remote 8 f9fca68f40783766b68a
make_day_branch_from 8 8

add_remote 9 3414496cc04909727a22
make_day_branch_from 9 9

add_remote 10 b1272e2fc69fed08d8fe
make_day_branch_from 10 10

add_remote 11 51eb7b7e70466095f879
make_day_branch_from 11 11

add_remote 12.1 5abdabc8bd0899886c88
add_remote 12.2 b11bfb45f3895aa39b2c
make_day_branch_from 12 12.1

add_remote 13 90556ac996e4f23e4d55
make_day_branch_from 13 13

add_remote 14 75f059f1d64b2f83c831
make_day_branch_from 14 14

add_remote 15 cefea3fa1c6ee4517aa0
make_day_branch_from 15 15

add_remote 16 08b49e329c9580201684
make_day_branch_from 16 16

add_remote 17 a8cefb87209737b1ebaa
make_day_branch_from 17 17

add_remote 18 8afda2aabb1b7043bfcb
make_day_branch_from 18 18

add_remote 19 9c8032bd2d5a26328e15
make_day_branch_from 19 19

add_remote 20 1e562b3793c2284173cf
make_day_branch_from 20 20

add_remote 21 fab575025661b73c5bea
make_day_branch_from 21 21

add_remote 22 52533b686357d4ae5d0b
make_day_branch_from 22 22

add_remote 23 67441392697ec8af61d2
make_day_branch_from 23 23

add_remote 24 cb1f57f9f6b1666aff23
make_day_branch_from 24 24

add_remote 25 da9965a20d2bf42554dd
make_day_branch_from 25 25
