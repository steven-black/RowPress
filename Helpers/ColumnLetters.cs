namespace Xemplate.Helpers;

public static class ColumnLetters
{
    public static int ToIndex(string letters)
    {
        int n = 0;
        foreach (char ch in letters.Trim().ToUpperInvariant())
        {
            // A = 65 and Z = 90
            if (ch < 'A' || ch > 'Z')
            {
                throw new FormatException($"'{letters}' is not a valid column.");
            }

            n = n * 26 + (ch - 'A' + 1);
        }

        return n - 1;
    }

    public static List<int> ParseList(string input) => 
        input.Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Select(ToIndex)
            .ToList();
}
