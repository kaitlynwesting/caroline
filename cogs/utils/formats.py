from discord.ext import commands


class LengthLimiter(commands.Converter):
    async def convert(self, ctx, argument):
        if len(argument) > 512:
            raise commands.BadArgument(f'Field is too long ({len(argument)}/512).')

        return argument
