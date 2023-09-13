from bluesky import __main__
import bluesky as bs


__main__.main()


# initialize bluesky as non-networked simulation node
bs.init(mode='sim', detached=True)


n = 3


bs.traf.mcre(n, actype="B744")


for acid in bs.traf.id:
    bs.stack.stack(f'ORIG {acid} EGLL;'
                   f'ADDWPT {acid} BPK FL60;'
                   f'ADDWPT {acid} TOTRI FL107;'
                   f'ADDWPT {acid} MATCH FL115;'
                   f'ADDWPT {acid} BRAIN FL164;'
                   f'VNAV {acid} ON')