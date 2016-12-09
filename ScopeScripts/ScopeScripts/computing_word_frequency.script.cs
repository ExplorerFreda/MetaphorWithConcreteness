using Microsoft.SCOPE.Types;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using ScopeRuntime;

using Newtonsoft.Json;

public class WordFrequencyProcessor : Processor
{
	public override Schema Produces(string[] requestedColumns, string[] args, Schema input)
	{
		Schema output = new Schema();
		output.Add(new ColumnInfo("Word", ColumnDataType.String));
		output.Add(new ColumnInfo("POSTag", ColumnDataType.String));
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
			for (int i = 0; i < tkss.Length; i++)
			{
				string word = sentence.Substring(tkss[i], tkes[i] - tkss[i]);
				outputRow["Word"].Set(word);
				outputRow["POSTag"].Set(poses[i]);
				outputRow["Count"].Set(1);
				yield return outputRow;
			}
		}
	}
}