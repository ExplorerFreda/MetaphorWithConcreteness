using Microsoft.SCOPE.Types;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using ScopeRuntime;

using Newtonsoft.Json;

using StringNormalization;

public class PatternProcessor : Processor
{
	public override Schema Produces(string[] requestedColumns, string[] args, Schema input)
	{
		Schema output = new Schema();
		output.Add(new ColumnInfo("Adjective", ColumnDataType.String));
		output.Add(new ColumnInfo("Noun", ColumnDataType.String));
		output.Add(new ColumnInfo("Count", ColumnDataType.Integer));
		return output;
	}
	public override IEnumerable<Row> Process(RowSet input, Row outputRow, string[] args)
	{
		foreach (Row row in input.Rows)
		{
			string sentence = row["Sentence"].String;
			int[] tkss = JsonConvert.DeserializeObject<int[]>(row["TokenStarts"].String);
			int[] tkes = JsonConvert.DeserializeObject<int[]>(row["TokenEnds"].String);
			string[] poses = JsonConvert.DeserializeObject<string[]>(row["POSTags"].String);
			if (tkss.Length != poses.Length || tkss.Length != tkes.Length)
			{
				Console.WriteLine("Error");
				continue;
			}
			for (int i = 0; i < tkss.Length - 1; i++)
			{
				string prev_word = sentence.Substring(tkss[i], tkes[i] - tkss[i]).ToLower();
				string succ_word = sentence.Substring(tkss[i + 1], tkes[i + 1] - tkss[i + 1]).ToLower();
				prev_word = StringNormalization.StringNormalization.MediateNormalization(prev_word);
				succ_word = StringNormalization.StringNormalization.MediateNormalization(succ_word);
				if (String.IsNullOrEmpty(prev_word) || String.IsNullOrEmpty(succ_word))
				{
					continue;
				}
				if (poses[i + 1].StartsWith("NN") && poses[i].StartsWith("JJ"))
				{
					outputRow["Adjective"].Set(prev_word);
					outputRow["Noun"].Set(succ_word);
					outputRow["Count"].Set(1);
					yield return outputRow;
				}
			}
		}
	}
}